# 🎯 Consistly

> Transform your drafts to match your brand's unique voice and style with AI-powered content editing.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 What is Consistly?

Consistly is a sophisticated tool that learns from your existing content to automatically edit and improve new drafts, maintaining consistent brand voice and writing style. Simply upload 3-5 reference articles that represent your ideal writing style, paste your draft, and let AI transform it to match your brand's unique voice.

### ✨ Key Features

- 🎨 **Style Learning**: Analyzes your reference articles to understand tone, structure, and voice
- 📄 **Multi-Format Support**: Works with PDF, DOCX, and TXT files
- ⚡ **Instant Results**: Get professionally edited content in under 2 minutes
- 🔒 **100% Private**: Runs locally with Ollama - your content never leaves your system
- 🎯 **Brand Consistency**: Maintains perfect consistency across all your content
- 💻 **Modern UI**: Beautiful, responsive interface with smooth animations

## 🏗️ Architecture

```
ai-writing-style-copier/
├── main.py                 # Application entry point
├── src/
│   ├── ai_engine.py       # AI processing and Ollama integration
│   ├── file_processor.py  # File handling and text extraction
│   ├── api_routes.py      # REST API endpoints
│   └── ui_components.py   # HTML template rendering
├── static/
│   ├── styles.css         # UI styles and design system
│   └── script.js          # Frontend JavaScript
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.com/) installed and running
- A compatible LLM model (we recommend `llama3:8b`)

### Step 1: Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the recommended model
ollama pull llama3:8b

# Start Ollama server
ollama serve
```

### Step 2: Set Up the Application

```bash
# Clone the repository
git clone https://github.com/your-username/ai-writing-style-copier.git
cd ai-writing-style-copier

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Step 3: Access the Application

Open your browser and navigate to `http://localhost:8000`

## 📖 How to Use

### 1. Upload Reference Articles
- Upload 3-5 articles that represent your ideal writing style
- Supports PDF, DOCX, and TXT formats
- Or paste content directly into text areas

### 2. Add Your Draft
- Upload or paste the article you want to improve
- The AI will analyze it for editing opportunities

### 3. Generate & Copy
- Click "Transform My Article" and wait for AI processing
- Copy the improved article with one click
- Use in your content workflow

## 🔧 API Documentation

The application provides a RESTful API with the following endpoints:

### Core Endpoints

- `GET /` - Main web interface
- `GET /api/health` - System health check
- `POST /api/extract-text` - Extract text from uploaded files
- `POST /api/generate-edit` - Complete style analysis and editing workflow

### Example API Usage

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/health")
print(response.json())

# Generate edited content
data = {
    "reference_articles": ["Article 1 text...", "Article 2 text..."],
    "draft_content": "Your draft text here..."
}
response = requests.post("http://localhost:8000/api/generate-edit", json=data)
result = response.json()
```

## 🚀 Deployment Options

### Option 1: Local Network Access
```bash
# Run on local network (others can access via your IP)
python main.py
# Access via http://YOUR_IP:8000
```

### Option 2: Hugging Face Spaces (Recommended)
1. Create account on [huggingface.co](https://huggingface.co)
2. Create new Space with "Gradio" template
3. Upload your code
4. Configure Ollama in the environment

### Option 3: Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

## ⚙️ Configuration

### Environment Variables

```bash
# Optional: Configure Ollama URL
export OLLAMA_URL="http://localhost:11434"

# Optional: Set default model
export OLLAMA_MODEL="llama3:8b"
```

### Customizing the AI Model

You can use different models by updating the `ai_engine.py` configuration:

```python
# For more powerful editing (requires more resources)
ai_engine = AIEngine(model="llama3:70b")

# For faster processing (less detailed editing)
ai_engine = AIEngine(model="llama3:3b")
```

## 🎨 Customization

### UI Theming

The application uses CSS custom properties for easy theming. Edit `static/styles.css`:

```css
:root {
  --primary-color: #your-brand-color;
  --secondary-color: #your-accent-color;
  /* ... other variables */
}
```

### Adding New File Formats

Extend the `FileProcessor` class in `src/file_processor.py`:

```python
def _extract_from_new_format(self, file_path: str) -> str:
    # Your extraction logic here
    pass
```

## 🔍 Troubleshooting

### Common Issues

**Ollama Connection Error**
- Ensure Ollama is running: `ollama serve`
- Check if the model is installed: `ollama list`

**File Processing Error**
- Verify file format is supported (PDF, DOCX, TXT)
- Check file size limits (10MB maximum)

**Slow Processing**
- Consider using a smaller model for faster results
- Ensure adequate RAM for the selected model

### Performance Optimization

- **RAM Usage**: 4-8GB when model is loaded
- **Processing Time**: 30-60 seconds per article
- **Storage**: ~5GB for model files

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy .
```

## 📊 System Requirements

### Minimum Requirements
- **CPU**: 4 cores, 2.5GHz
- **RAM**: 8GB
- **Storage**: 10GB free space
- **OS**: Linux, macOS, Windows

### Recommended Requirements
- **CPU**: 8 cores, 3.0GHz+
- **RAM**: 16GB+
- **Storage**: 20GB+ SSD
- **GPU**: Optional, for faster processing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) for local LLM infrastructure
- [FastAPI](https://fastapi.tiangolo.com/) for the robust web framework
- [Hugging Face](https://huggingface.co/) for deployment platform

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/ashutoshgautams/ai-writing-style-copier/issues)
- **Custom Solutions**: [LinkedIn - Ashutosh Gautam](https://www.linkedin.com/in/ashutosh-gautam-3747b3179/)
- **Documentation**: Check the `/api/docs` endpoint when running

---

**Built with ❤️ by [Ashutosh Gautam](https://www.linkedin.com/in/ashutosh-gautam-3747b3179/) • Open Source • Privacy First**
