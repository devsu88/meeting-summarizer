# 🎯 Meeting Summarizer

An **interactive web app** with **Gradio** that allows you to upload a meeting transcript or audio/video file and automatically generates a **complete summary**, **topics** list, and **keywords**.

## 🌐 Live Demo

🚀 **[Try the app on Hugging Face Spaces](https://huggingface.co/spaces/devsu/meeting-summarizer)**

## 🚀 Features

- 📁 **Multiple uploads**: Supports `.txt`, `.pdf`, `.docx`, `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` files
- 🎤 **Automatic transcription**: Uses `whisper-tiny` to transcribe audio files
- 🤖 **Intelligent analysis**: GPT-4o-mini to extract summaries, topics and keywords
- 📄 **Professional PDF**: Generates well-formatted PDF documents
- 💾 **Data persistence**: Save to Hugging Face Datasets
- 🌐 **Easy deployment**: Ready for Hugging Face Spaces

## 🛠️ Technologies

- **UI Framework**: [Gradio](https://gradio.app/)
- **LLM**: `gpt-4o-mini` via OpenAI API
- **Transcription**: `openai/whisper-tiny` (CPU optimized)
- **Text extraction**: `pypdf2` and `python-docx`
- **PDF generation**: `reportlab`
- **Persistence**: Hugging Face Datasets
- **Audio processing**: `librosa` for audio processing
- **Acceleration**: `accelerate` for optimizations
- **Language**: Python 3.10

## 📦 Installation

### Local

```bash
# Clone the repository
git clone https://github.com/your-username/meeting-summarizer.git
cd meeting-summarizer

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

### Hugging Face Spaces

1. **Fork** this repository
2. Create a new **Space** on [Hugging Face](https://huggingface.co/spaces)
3. Select **Gradio** as SDK
4. Link the forked repository
5. Configure environment variables (see Configuration section)

## ⚙️ Configuration

### Environment Variables

For deployment on Hugging Face Spaces, configure:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for data persistence)
HF_TOKEN=your_huggingface_token_here
```

### Local Configuration

Environment variables can be set directly in the system or through the web application interface.

## 🎯 Usage

1. **Upload a meeting file** (audio or document)
2. **Enter OpenAI API key** (required)
3. **Enter HF token** (optional, to save data)
4. **Click "Analyze Meeting"**
5. **View results** and download PDF

### Supported Formats

#### 🎵 Audio Files
- MP3, WAV, M4A, FLAC, OGG
- Automatic transcription with Whisper

#### 📄 Documents
- PDF, DOCX, TXT
- Automatic text extraction

## 📊 Data Structure

Meetings are saved to Hugging Face Datasets with this structure:

```json
{
  "id": "uuid",
  "file_name": "original_file_name",
  "meeting_date": "YYYY-MM-DD",
  "transcription": "complete meeting text",
  "summary": "summary text",
  "topics": ["topic1", "topic2", ...],
  "keywords": ["keyword1", "keyword2", ...],
  "created_at": "timestamp"
}
```

## 🏗️ Architecture

```
meeting-summarizer/
├── app.py                 # Main Gradio application
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── .gitignore            # Files to ignore
├── data/                 # Example files and data
│   └── sample_meeting_transcript.txt
└── utils/
    ├── __init__.py
    ├── text_extraction.py   # Text extraction from PDF/DOCX/TXT
    ├── transcription.py     # Audio transcription with Whisper
    ├── llm_analysis.py       # Analysis with GPT-4o-mini
    ├── pdf_generator.py     # PDF output generation
    └── data_persistence.py # Save to HF Datasets
```

## 🔧 Development

### Development Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start in development mode
python app.py
```

### Testing

```bash
# Test text extraction
python -c "from utils.text_extraction import extract_text; print(extract_text('test.pdf'))"

# Test transcription
python -c "from utils.transcription import transcribe_audio; print(transcribe_audio('test.mp3'))"
```

## 📝 Technical Notes

- **Whisper**: Uses `openai/whisper-tiny` for CPU speed
- **Language**: Prompts optimized for Italian
- **Persistence**: HF Datasets ensures permanent storage
- **Security**: API keys managed via environment variables
- **Compatibility**: Python 3.10, optimized for CPU only

## 🤝 Contributing

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🆘 Support

- 📧 **Email**: support@meeting-summarizer.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/meeting-summarizer/issues)
- 📖 **Documentation**: [Wiki](https://github.com/your-username/meeting-summarizer/wiki)

## 🙏 Acknowledgments

- [Gradio](https://gradio.app/) for the UI framework
- [OpenAI](https://openai.com/) for GPT-4o-mini and Whisper
- [Hugging Face](https://huggingface.co/) for models and hosting
- [ReportLab](https://www.reportlab.com/) for PDF generation

---

**Developed with ❤️ to simplify meeting analysis**