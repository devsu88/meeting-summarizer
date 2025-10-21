"""
Module for saving meeting data to Hugging Face Datasets.
Manages permanent persistence of analysis results.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Optional

try:
    from datasets import Dataset
    from huggingface_hub import HfApi, login
except ImportError:
    Dataset = None
    HfApi = None
    login = None

# Configurazione logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nome del dataset su Hugging Face
DATASET_NAME = "meeting-summarizer-data"


def save_meeting_to_dataset(meeting_data: Dict, hf_token: Optional[str] = None) -> bool:
    """
    Save meeting data to Hugging Face Dataset.
    
    Args:
        meeting_data (Dict): Meeting data to save
        hf_token (Optional[str]): Hugging Face token (optional)
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    if not meeting_data:
        logger.error("Meeting data not provided")
        return False
    
    if Dataset is None:
        logger.error("datasets not installed. Install with: pip install datasets")
        return False
    
    try:
        # Authentication if token provided
        if hf_token:
            try:
                login(token=hf_token)
                logger.info("Hugging Face authentication completed")
            except Exception as e:
                logger.warning(f"Error in HF authentication: {str(e)}")
                logger.info("Continuing without authentication...")
        
        # Prepare data for saving
        meeting_record = _prepare_meeting_record(meeting_data)
        
        # Create or load dataset
        dataset = _get_or_create_dataset()
        
        # Add new record
        if dataset is None:
            logger.error("Unable to create or load dataset")
            return False
        
        # Convert dataset to list to add record
        records = list(dataset)
        records.append(meeting_record)
        
        # Create new dataset with added record
        new_dataset = Dataset.from_list(records)
        
        # Push to Hugging Face Hub (if authenticated)
        if hf_token:
            try:
                new_dataset.push_to_hub(
                    DATASET_NAME,
                    private=True,
                    token=hf_token
                )
                logger.info(f"Dataset updated on Hugging Face Hub: {DATASET_NAME}")
            except Exception as e:
                logger.warning(f"Unable to push to HF Hub: {str(e)}")
                logger.info("Data saved locally")
        
        logger.info("Meeting saved successfully to dataset")
        return True
        
    except Exception as e:
        logger.error(f"Error while saving meeting: {str(e)}")
        return False


def _prepare_meeting_record(meeting_data: Dict) -> Dict:
    """
    Prepare meeting record for saving.
    
    Args:
        meeting_data (Dict): Meeting data
        
    Returns:
        Dict: Record formatted for dataset
    """
    current_time = datetime.now()
    
    return {
        "id": str(uuid.uuid4()),
        "file_name": meeting_data.get("file_name", "unknown"),
        "meeting_date": current_time.strftime("%Y-%m-%d"),
        "transcription": meeting_data.get("transcription", ""),
        "summary": meeting_data.get("summary", ""),
        "topics": json.dumps(meeting_data.get("topics", [])),
        "keywords": json.dumps(meeting_data.get("keywords", [])),
        "created_at": current_time.isoformat()
    }


def _get_or_create_dataset() -> Optional[Dataset]:
    """
    Create or load Hugging Face dataset.
    
    Returns:
        Optional[Dataset]: Dataset or None if error
    """
    try:
        # Try to load existing dataset
        try:
            dataset = Dataset.from_hub(DATASET_NAME)
            logger.info(f"Existing dataset loaded: {DATASET_NAME}")
            return dataset
        except Exception:
            logger.info(f"Dataset {DATASET_NAME} not found, creating new dataset...")
        
        # Create new empty dataset
        empty_dataset = Dataset.from_dict({
            "id": [],
            "file_name": [],
            "meeting_date": [],
            "transcription": [],
            "summary": [],
            "topics": [],
            "keywords": [],
            "created_at": []
        })
        
        logger.info(f"New dataset created: {DATASET_NAME}")
        return empty_dataset
        
    except Exception as e:
        logger.error(f"Error in creating/loading dataset: {str(e)}")
        return None


def load_meetings_from_dataset(hf_token: Optional[str] = None) -> Optional[list]:
    """
    Load all meetings from dataset.
    
    Args:
        hf_token (Optional[str]): Hugging Face token
        
    Returns:
        Optional[list]: List of meetings or None if error
    """
    if Dataset is None:
        logger.error("datasets not installed")
        return None
    
    try:
        # Authentication if token provided
        if hf_token:
            try:
                login(token=hf_token)
            except Exception as e:
                logger.warning(f"Error in HF authentication: {str(e)}")
        
        # Load dataset
        dataset = Dataset.from_hub(DATASET_NAME)
        
        # Convert to list
        meetings = list(dataset)
        
        logger.info(f"Loaded {len(meetings)} meetings from dataset")
        return meetings
        
    except Exception as e:
        logger.error(f"Error loading meetings: {str(e)}")
        return None


def get_dataset_info() -> Dict:
    """
    Return dataset information.
    
    Returns:
        Dict: Dataset information
    """
    return {
        "dataset_name": DATASET_NAME,
        "description": "Dataset for persisting analyzed meetings",
        "fields": [
            "id", "file_name", "meeting_date", "transcription", 
            "summary", "topics", "keywords", "created_at"
        ]
    }
