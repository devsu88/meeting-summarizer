# 🎯 Meeting Summarizer

Una **web app interattiva** con **Gradio** che permette di caricare una trascrizione o un file audio/video di un meeting e genera automaticamente una **sintesi completa**, un elenco di **topic** e **parole chiave**.

## 🚀 Funzionalità

- 📁 **Upload multipli**: Supporta file `.txt`, `.pdf`, `.docx`, `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`
- 🎤 **Trascrizione automatica**: Usa `whisper-tiny` per trascrivere file audio
- 🤖 **Analisi intelligente**: GPT-4o-mini per estrarre sintesi, topic e keywords
- 📄 **PDF professionale**: Genera documenti PDF ben formattati
- 💾 **Persistenza dati**: Salvataggio su Hugging Face Datasets
- 🌐 **Deploy facile**: Pronto per Hugging Face Spaces

## 🛠️ Tecnologie

- **Framework UI**: [Gradio](https://gradio.app/)
- **LLM**: `gpt-4o-mini` tramite API OpenAI
- **Trascrizione**: `openai/whisper-tiny` (ottimizzato per CPU)
- **Estrazione testo**: `pypdf2` e `python-docx`
- **Generazione PDF**: `reportlab`
- **Persistenza**: Hugging Face Datasets
- **Audio processing**: `librosa` per elaborazione audio
- **Accelerazione**: `accelerate` per ottimizzazioni
- **Linguaggio**: Python 3.10

## 📦 Installazione

### Locale

```bash
# Clona il repository
git clone https://github.com/your-username/meeting-summarizer.git
cd meeting-summarizer

# Installa dipendenze
pip install -r requirements.txt

# Avvia l'applicazione
python app.py
```

### Hugging Face Spaces

1. **Fork** questo repository
2. Crea un nuovo **Space** su [Hugging Face](https://huggingface.co/spaces)
3. Seleziona **Gradio** come SDK
4. Collega il repository forked
5. Configura le variabili d'ambiente (vedi sezione Configurazione)

## ⚙️ Configurazione

### Variabili d'Ambiente

Per il deploy su Hugging Face Spaces, configura:

```bash
# Obbligatorio
OPENAI_API_KEY=your_openai_api_key_here

# Opzionale (per persistenza dati)
HF_TOKEN=your_huggingface_token_here
```

### Configurazione Locale

Crea un file `.env` nella root del progetto:

```bash
OPENAI_API_KEY=your_openai_api_key_here
HF_TOKEN=your_huggingface_token_here
```

## 🎯 Utilizzo

1. **Carica un file** di meeting (audio o documento)
2. **Inserisci la chiave API OpenAI** (richiesta)
3. **Inserisci il token HF** (opzionale, per salvare i dati)
4. **Clicca "Analizza Meeting"**
5. **Visualizza i risultati** e scarica il PDF

### Formati Supportati

#### 🎵 File Audio
- MP3, WAV, M4A, FLAC, OGG
- Trascrizione automatica con Whisper

#### 📄 Documenti
- PDF, DOCX, TXT
- Estrazione testo automatica

## 📊 Struttura Dati

I meeting vengono salvati su Hugging Face Datasets con questa struttura:

```json
{
  "id": "uuid",
  "file_name": "nome_file_originale",
  "meeting_date": "YYYY-MM-DD",
  "transcription": "testo completo del meeting",
  "summary": "testo della sintesi",
  "topics": ["tema1", "tema2", ...],
  "keywords": ["parola1", "parola2", ...],
  "created_at": "timestamp"
}
```

## 🏗️ Architettura

```
meeting-summarizer/
├── app.py                 # Applicazione Gradio principale
├── requirements.txt       # Dipendenze Python
├── README.md             # Documentazione
├── .gitignore            # File da ignorare
└── utils/
    ├── __init__.py
    ├── text_extraction.py   # Estrazione testo da PDF/DOCX/TXT
    ├── transcription.py     # Trascrizione audio con Whisper
    ├── llm_analysis.py       # Analisi con GPT-4o-mini
    ├── pdf_generator.py     # Generazione PDF output
    └── data_persistence.py # Salvataggio su HF Datasets
```

## 🔧 Sviluppo

### Setup Ambiente di Sviluppo

```bash
# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt

# Avvia in modalità sviluppo
python app.py
```

### Test

```bash
# Test estrazione testo
python -c "from utils.text_extraction import extract_text; print(extract_text('test.pdf'))"

# Test trascrizione
python -c "from utils.transcription import transcribe_audio; print(transcribe_audio('test.mp3'))"
```

## 📝 Note Tecniche

- **Whisper**: Usa `openai/whisper-tiny` per velocità su CPU
- **Lingua**: Prompt ottimizzati per italiano
- **Persistenza**: HF Datasets garantisce storage permanente
- **Sicurezza**: API keys gestite tramite variabili d'ambiente
- **Compatibilità**: Python 3.10, ottimizzato per CPU only

## 🤝 Contributi

1. Fork il progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 🆘 Supporto

- 📧 **Email**: support@meeting-summarizer.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/meeting-summarizer/issues)
- 📖 **Documentazione**: [Wiki](https://github.com/your-username/meeting-summarizer/wiki)

## 🙏 Ringraziamenti

- [Gradio](https://gradio.app/) per il framework UI
- [OpenAI](https://openai.com/) per GPT-4o-mini e Whisper
- [Hugging Face](https://huggingface.co/) per i modelli e l'hosting
- [ReportLab](https://www.reportlab.com/) per la generazione PDF

---

**Sviluppato con ❤️ per semplificare l'analisi dei meeting**