"""
Module for generating PDF reports with meeting analysis results.
Uses reportlab to create well-formatted documents.
"""

import os
import tempfile
from datetime import datetime
from typing import Dict, Optional

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib import colors
except ImportError:
    A4 = None
    getSampleStyleSheet = None
    ParagraphStyle = None
    inch = None
    SimpleDocTemplate = None
    Paragraph = None
    Spacer = None
    PageBreak = None
    colors = None

# Configurazione logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_pdf(meeting_data: Dict) -> Optional[str]:
    """
    Generate a PDF with meeting analysis results.
    
    Args:
        meeting_data (Dict): Meeting data with summary, topics, keywords
        
    Returns:
        Optional[str]: Path to generated PDF file or None if error
    """
    if not meeting_data:
        logger.error("Meeting data not provided")
        return None
    
    if SimpleDocTemplate is None:
        logger.error("reportlab not installed. Install with: pip install reportlab")
        return None
    
    try:
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"meeting_summary_{timestamp}.pdf"
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Custom styles
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Centered
            textColor=colors.darkblue
        )
        
        # Section style
        section_style = ParagraphStyle(
            'CustomSection',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue
        )
        
        # Normal text style
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leading=14
        )
        
        # List style
        list_style = ParagraphStyle(
            'CustomList',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=3,
            leftIndent=20,
            bulletIndent=10
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph("Meeting Summary", title_style))
        story.append(Spacer(1, 12))
        
        # Date and info
        current_date = datetime.now().strftime("%m/%d/%Y %H:%M")
        story.append(Paragraph(f"<b>Analysis date:</b> {current_date}", normal_style))
        story.append(Spacer(1, 20))
        
        # Summary
        story.append(Paragraph("Summary", section_style))
        summary_text = meeting_data.get("summary", "Summary not available")
        story.append(Paragraph(summary_text, normal_style))
        story.append(Spacer(1, 20))
        
        # Main topics
        story.append(Paragraph("Main Topics", section_style))
        topics = meeting_data.get("topics", [])
        if topics:
            for topic in topics:
                story.append(Paragraph(f"• {topic}", list_style))
        else:
            story.append(Paragraph("Topics not available", normal_style))
        story.append(Spacer(1, 20))
        
        # Keywords
        story.append(Paragraph("Keywords", section_style))
        keywords = meeting_data.get("keywords", [])
        if keywords:
            # Group keywords in rows of 3-4
            keyword_lines = []
            for i in range(0, len(keywords), 4):
                line_keywords = keywords[i:i+4]
                keyword_lines.append(" • ".join(line_keywords))
            
            for line in keyword_lines:
                story.append(Paragraph(f"• {line}", list_style))
        else:
            story.append(Paragraph("Keywords not available", normal_style))
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            f"<i>Automatically generated on {current_date} by Meeting Summarizer</i>",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=1)
        ))
        
        # Generate PDF
        doc.build(story)
        
        logger.info(f"PDF generated successfully: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        logger.error(f"Error during PDF generation: {str(e)}")
        return None


def cleanup_temp_pdf(pdf_path: str) -> None:
    """
    Clean up temporary PDF file.
    
    Args:
        pdf_path (str): Path to PDF file to delete
    """
    try:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            logger.info(f"Temporary PDF file deleted: {pdf_path}")
    except Exception as e:
        logger.warning(f"Unable to delete temporary PDF file {pdf_path}: {str(e)}")
