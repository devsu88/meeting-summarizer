"""
Meeting Summarizer - Applicazione Gradio
Web app per l'analisi e sintesi automatica di meeting tramite GPT-4o-mini.
"""

import os
import tempfile
import shutil
import gradio as gr
from typing import Tuple, Optional

# Import moduli locali
from utils.text_extraction import extract_text, get_supported_extensions
from utils.transcription import transcribe_audio, is_audio_file, get_supported_audio_extensions
from utils.llm_analysis import analyze_meeting, format_analysis_for_display
from utils.pdf_generator import generate_pdf, cleanup_temp_pdf
from utils.data_persistence import save_meeting_to_dataset

# Configurazione logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variabili globali per file temporanei
_temp_files = []



def process_meeting(file, api_key: str, hf_token: str = "") -> Tuple[str, str, str, str, str]:
    """
    Processa un file di meeting e restituisce l'analisi completa.
    
    Args:
        file: File caricato dall'utente
        api_key (str): Chiave API OpenAI
        hf_token (str): Token Hugging Face (opzionale)
        
    Returns:
        Tuple[str, str, str, str, str]: (summary, topics, keywords, pdf_path, message)
    """
    global _temp_files

    try:
        # Verifica input e debug
        logger.info(f"DEBUG: file ricevuto tipo={type(file)} valore={file}")
        
        if not file:
            return "", "", "", None, "❌ Error: No file uploaded"
        
        if not api_key:
            return "", "", "", None, "❌ Error: OpenAI API key required"
        
        # Gestisci l'oggetto file di Gradio
        # Nelle versioni recenti di Gradio, il file può essere una stringa (path) o un oggetto
        if isinstance(file, str):
            file_path = file
        else:
            # Se è un oggetto file, estrai il path
            file_path = file.name if hasattr(file, 'name') else str(file)
        
        logger.info(f"DEBUG: file_path={file_path} exists={os.path.exists(file_path)} isfile={os.path.isfile(file_path) if os.path.exists(file_path) else 'N/A'}")
        
        # Verify that the file exists and is a file (not a directory)
        if not os.path.exists(file_path):
            return "", "", "", None, "❌ Error: File not found or invalid"
        
        if not os.path.isfile(file_path):
            return "", "", "", None, f"❌ Error: Path is a directory, not a file: {file_path}"
        
        # Estrai testo dal file
        text = ""
        file_name = os.path.basename(file_path)
        
        logger.info(f"Processamento file: {file_name}")
        logger.info(f"Percorso file: {file_path}")
        
        # Determine if it's an audio file
        if is_audio_file(file_name):
            logger.info("Audio file detected, starting transcription...")
            text = transcribe_audio(file_path)
            if not text:
                return "", "", "", None, "❌ Error: Transcription failed"
            logger.info("Transcription completed")
        else:
            # Extract text from document
            logger.info("Document file detected, extracting text...")
            text = extract_text(file_path)
            if not text:
                return "", "", "", None, "❌ Error: Text extraction failed"
            logger.info("Text extraction completed")
        
        # Verify that the text is not empty
        if not text.strip():
            return "", "", "", None, "❌ Error: No text extracted from file"
        
        # Analyze with GPT-4o-mini
        logger.info("Starting analysis with GPT-4o-mini...")
        analysis = analyze_meeting(text, api_key)
        if not analysis:
            return "", "", "", None, "❌ Error: Analysis failed"
        
        # Formatta per display
        formatted_analysis = format_analysis_for_display(analysis)
        
        # Generate PDF
        logger.info("Generating PDF...")
        pdf_path = generate_pdf(analysis)
        
        # Debug: verify that pdf_path is valid
        if pdf_path:
            logger.info(f"PDF generated: {pdf_path}")
            logger.info(f"PDF exists: {os.path.exists(pdf_path)}")
            logger.info(f"PDF is a file: {os.path.isfile(pdf_path)}")
            # If not a valid file, set to None
            if not os.path.isfile(pdf_path):
                logger.warning(f"PDF path invalid: {pdf_path}")
                pdf_path = None
        
        # Save to dataset if token provided
        if hf_token:
            logger.info("Saving to Hugging Face Dataset...")
            meeting_data = {
                "file_name": file_name,
                "transcription": text,
                "summary": analysis.get("summary", ""),
                "topics": analysis.get("topics", []),
                "keywords": analysis.get("keywords", [])
            }
            
            if save_meeting_to_dataset(meeting_data, hf_token):
                logger.info("Meeting saved to HF Dataset")
            else:
                logger.warning("Saving to HF Dataset failed")
        
        # Add PDF to temporary files for cleanup
        if pdf_path:
            _temp_files.append(pdf_path)
        
        # Success message
        success_msg = f"✅ Meeting analyzed successfully!\n\n📄 File: {file_name}\n📝 Characters analyzed: {len(text)}\n📊 Topics identified: {len(analysis.get('topics', []))}\n🔑 Keywords: {len(analysis.get('keywords', []))}"
        
        if hf_token:
            success_msg += "\n💾 Data saved to Hugging Face Dataset"
        
        return (
            formatted_analysis["summary"],
            formatted_analysis["topics"], 
            formatted_analysis["keywords"],
            pdf_path if pdf_path else None,
            success_msg
        )
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        return "", "", "", None, f"❌ Error: {str(e)}"


def cleanup_temp_files():
    """Clean up temporary files."""
    global _temp_files
    for file_path in _temp_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                logger.warning(f"Unable to delete {file_path}: {str(e)}")
    _temp_files.clear()


def create_interface():
    """Create the Gradio interface."""
    
    # Supported extensions
    supported_extensions = get_supported_extensions() + get_supported_audio_extensions()
    
    with gr.Blocks(
        title="Meeting Summarizer",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .success-message {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 10px;
            border-radius: 5px;
        }
        """
    ) as app:
        
        gr.Markdown(
            """
            # 🎯 Meeting Summarizer
            
            Upload a meeting file (audio, PDF, DOCX, TXT) and automatically get:
            - 📝 **Complete summary** of the meeting
            - 🏷️ **Main topics** discussed  
            - 🔑 **Relevant keywords**
            - 📄 **Downloadable PDF** with all results
            
            ---
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                # Input file
                file_input = gr.File(
                    label="📁 Upload Meeting File",
                    file_types=supported_extensions,
                    file_count="single"
                )
                
                # API Key OpenAI
                api_key_input = gr.Textbox(
                    label="🔑 OpenAI API Key",
                    placeholder="Enter your OpenAI API key...",
                    type="password",
                    info="Required for analysis with GPT-4o-mini"
                )
                
                # HF Token (optional)
                hf_token_input = gr.Textbox(
                    label="🤗 Hugging Face Token (Optional)",
                    placeholder="Enter your HF token to save data...",
                    type="password",
                    info="Optional: to save results to Hugging Face Dataset"
                )
                
                # Analyze button
                analyze_btn = gr.Button(
                    "🚀 Analyze Meeting",
                    variant="primary",
                    size="lg"
                )
                
                # Status message
                status_msg = gr.Textbox(
                    label="📊 Status",
                    interactive=False,
                    visible=True
                )
            
            with gr.Column(scale=2):
                # Output summary
                summary_output = gr.Markdown(
                    label="📝 Meeting Summary",
                    value="The summary will appear here after analysis..."
                )
                
                # Output topics
                topics_output = gr.Markdown(
                    label="🏷️ Main Topics",
                    value="The main topics will appear here..."
                )
                
                # Output keywords
                keywords_output = gr.Markdown(
                    label="🔑 Keywords",
                    value="The keywords will appear here..."
                )
                
                # Download PDF
                pdf_download = gr.File(
                    label="📄 Download PDF Report",
                    visible=True
                )
        
        # Footer
        gr.Markdown(
            """
            ---
            ### ℹ️ Information
            
            **Supported formats:**
            - 🎵 **Audio**: MP3, WAV, M4A, FLAC, OGG
            - 📄 **Documents**: PDF, DOCX, TXT
            
            **Features:**
            - 🎤 Automatic audio transcription with Whisper
            - 🤖 Intelligent analysis with GPT-4o-mini
            - 📊 Topic and keyword extraction
            - 💾 Save to Hugging Face Datasets
            - 📄 Professional PDF generation
            
            **Notes:**
            - Audio files are automatically transcribed
            - Analysis is optimized for meetings
            - Data is saved only if you provide an HF token
            """
        )
        
        # Eventi
        analyze_btn.click(
            fn=process_meeting,
            inputs=[file_input, api_key_input, hf_token_input],
            outputs=[summary_output, topics_output, keywords_output, pdf_download, status_msg],
            show_progress=True
        )
        
        # Cleanup al chiudere
        app.unload(cleanup_temp_files)
    
    return app


def main():
    """Main function."""
    logger.info("Starting Meeting Summarizer...")
    
    # Create interface
    app = create_interface()
    
    # Launch server
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )


if __name__ == "__main__":
    main()
