"""
Module for transcribing audio files using Whisper.
Optimized for CPU with whisper-tiny model.
"""

import os
import logging
from typing import Optional

try:
    import torch
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
    import librosa
except ImportError as e:
    print(f"Import error: {e}")
    torch = None
    WhisperProcessor = None
    WhisperForConditionalGeneration = None
    librosa = None

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variabili globali per il modello (caricato una sola volta)
_model = None
_processor = None


def load_whisper_model():
    """Load Whisper tiny model optimized for CPU."""
    global _model, _processor
    
    if _model is None or _processor is None:
        try:
            logger.info("Loading Whisper tiny model...")
            
            # Load processor and model
            _processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
            _model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
            
            # Configure for CPU
            _model.eval()
            if torch.cuda.is_available():
                _model = _model.to("cuda")
            else:
                _model = _model.to("cpu")
            
            logger.info("Whisper model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading Whisper model: {str(e)}")
            raise
    
    return _model, _processor


def transcribe_audio(file_path: str, language: str = "en") -> Optional[str]:
    """
    Transcribe an audio file using Whisper.
    
    Args:
        file_path (str): Path to audio file
        language (str): Language of audio content (default: "en" for English)
        
    Returns:
        Optional[str]: Text transcription or None if error
    """
    if not os.path.exists(file_path):
        logger.error(f"Audio file not found: {file_path}")
        return None
    
    if librosa is None:
        logger.error("librosa not installed. Install with: pip install librosa")
        return None
    
    try:
        # Load the model
        model, processor = load_whisper_model()
        
        # Load and preprocess audio
        logger.info(f"Loading audio file: {file_path}")
        audio_array, sample_rate = librosa.load(file_path, sr=16000)
        
        # Preprocess audio
        inputs = processor(audio_array, sampling_rate=sample_rate, return_tensors="pt")
        
        # Move to appropriate device
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate transcription
        logger.info("Generating transcription...")
        with torch.no_grad():
            predicted_ids = model.generate(
                inputs["input_features"],
                max_length=448,
                num_beams=1,
                do_sample=False,
                language=language
            )
        
        # Decode the result
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        
        logger.info("Transcription completed successfully")
        return transcription.strip()
        
    except Exception as e:
        logger.error(f"Error during transcription of {file_path}: {str(e)}")
        return None


def get_supported_audio_extensions() -> list:
    """Return supported audio extensions."""
    return ['.mp3', '.wav', '.m4a', '.flac', '.ogg']


def is_audio_file(file_path: str) -> bool:
    """Check if a file is a supported audio file."""
    if not file_path:
        return False
    
    file_extension = os.path.splitext(file_path)[1].lower()
    return file_extension in get_supported_audio_extensions()
