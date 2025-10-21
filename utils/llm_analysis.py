"""
Module for analyzing meeting text using GPT-4o-mini.
Extracts summary, topics and keywords from text.
"""

import json
import logging
from typing import Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_meeting(text: str, api_key: str) -> Optional[Dict]:
    """
    Analyze meeting text using GPT-4o-mini.
    
    Args:
        text (str): Meeting text to analyze
        api_key (str): OpenAI API key
        
    Returns:
        Optional[Dict]: Dictionary with summary, topics, keywords or None if error
    """
    if not text or not text.strip():
        logger.error("Empty text provided for analysis")
        return None
    
    if not api_key:
        logger.error("OpenAI API key not provided")
        return None
    
    if OpenAI is None:
        logger.error("OpenAI not installed. Install with: pip install openai")
        return None
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Structured prompt for analysis
        prompt = f"""
Analyze the following meeting text and provide a response in JSON format with the following keys:

1. "summary": A comprehensive and detailed summary of the meeting (minimum 200 words)
2. "topics": A list of 5-8 main topics discussed in the meeting
3. "keywords": A list of 10-15 relevant keywords

Meeting text:
{text}

Respond ONLY with the requested JSON, without any additional text.
"""

        logger.info("Sending request to GPT-4o-mini...")
        
        # API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert assistant in meeting analysis. Always provide responses in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        # Extract response content
        content = response.choices[0].message.content.strip()
        
        # Clean content from any markdown or extra text
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        # Parse JSON
        try:
            result = json.loads(content)
            
            # Structure validation
            required_keys = ["summary", "topics", "keywords"]
            if not all(key in result for key in required_keys):
                logger.error("Invalid JSON structure: missing keys")
                return None
            
            # Type validation
            if not isinstance(result["summary"], str):
                logger.error("Summary must be a string")
                return None
            if not isinstance(result["topics"], list):
                logger.error("Topics must be a list")
                return None
            if not isinstance(result["keywords"], list):
                logger.error("Keywords must be a list")
                return None
            
            logger.info("Analysis completed successfully")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Received content: {content}")
            return None
        
    except Exception as e:
        logger.error(f"Error during meeting analysis: {str(e)}")
        return None


def format_analysis_for_display(analysis: Dict) -> Dict[str, str]:
    """
    Format analysis for display in Gradio.
    
    Args:
        analysis (Dict): Analysis result
        
    Returns:
        Dict[str, str]: Dictionary formatted for display
    """
    if not analysis:
        return {
            "summary": "Error in analysis",
            "topics": "Error in analysis", 
            "keywords": "Error in analysis"
        }
    
    # Format topics as markdown list
    topics_md = "\n".join([f"- {topic}" for topic in analysis.get("topics", [])])
    
    # Format keywords as markdown list
    keywords_md = "\n".join([f"- {keyword}" for keyword in analysis.get("keywords", [])])
    
    return {
        "summary": analysis.get("summary", "Summary not available"),
        "topics": topics_md,
        "keywords": keywords_md
    }
