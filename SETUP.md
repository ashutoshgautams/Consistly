# 🏠 Consistly - Local Setup Instructions

## Privacy-First Local Deployment

This guide will help you set up Consistly completely locally on your machine, ensuring **100% privacy** - your content never leaves your device.

## 📋 Prerequisites

- **Python 3.8+** 
- **Git**
- **8GB+ RAM** (for running local AI models)
- **10GB+ free disk space** (for AI models)

## 🚀 Quick Start

### Step 1: Install Ollama (Local AI Engine)

**For macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**For Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**For Windows:**
1. Download from [ollama.ai](https://ollama.ai/download)
2. Run the installer
3. Open PowerShell/CMD as Administrator

### Step 2: Download AI Model

```bash
# Start Ollama (keep this running)
ollama serve

# In a new terminal, download the model
ollama pull llama3.1:8b
```

> **Note:** First download will take 5-10 minutes (4.7GB model)

### Step 3: Clone Consistly

```bash
git clone https://github.com/your-username/consistly.git
cd consistly
```

### Step 4: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Run Consistly

```bash
# Make sure Ollama is running (ollama serve)
python main.py
```

🎉 **Open http://localhost:8000 in your browser!**

---

## 📁 Project Structure

```
consistly/
├── main.py              # FastAPI backend
├── ui_components.py     # UI renderer (your existing file)
├── requirements.txt     # Python dependencies
├── static/             # CSS/JS assets
├── templates/          # HTML templates
└── api/
    ├── __init__.py
    ├── routes.py       # API endpoints
    └── llm_service.py  # Ollama integration
```

---

## 🔧 Configuration

Create `.env` file in project root:

```env
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# App Configuration  
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# Privacy Mode
LOCAL_ONLY=True
LOG_REQUESTS=False
```

---

## 🛠️ Advanced Setup

### Using Different Models

```bash
# For better quality (requires 16GB+ RAM)
ollama pull llama3.1:70b

# For faster processing (4GB RAM)  
ollama pull llama3.1:7b

# Update .env file with your chosen model
```

### Performance Tuning

```bash
# Check GPU availability
ollama list

# Monitor resources
htop  # Linux/macOS
# Task Manager on Windows
```

---

## 🔒 Privacy Verification

To verify your setup is truly private:

1. **Disconnect internet** after setup
2. **Process content** - it should still work
3. **Check network traffic** - no external calls should be made

### Network Monitoring (Optional)

```bash
# Monitor network connections (macOS/Linux)
lsof -i :8000  # Should only show local connections

# Windows
netstat -an | findstr :8000
```

---

## 🚨 Troubleshooting

### Ollama Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Restart Ollama
pkill ollama
ollama serve

# Check logs
tail -f ~/.ollama/logs/server.log
```

### Python Issues

```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear cache
pip cache purge
```

### Memory Issues

```bash
# Check available memory
free -h  # Linux
vm_stat  # macOS

# Use smaller model if needed
ollama pull llama3.1:7b
```

### Port Conflicts

```bash
# Check what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use different port
python main.py --port 8001
```

---

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8GB | 16GB+ |
| CPU | 4 cores | 8+ cores |
| Storage | 10GB | 20GB+ |
| GPU | None | NVIDIA (CUDA) |

---

## 🔄 Updates

```bash
# Update Consistly
git pull origin main
pip install --upgrade -r requirements.txt

# Update Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Update models
ollama pull llama3.1:8b
```

---

## 💡 Tips for Best Performance

1. **Close other applications** to free up RAM
2. **Use SSD storage** for faster model loading
3. **Enable GPU acceleration** if available
4. **Process smaller batches** if experiencing slowdowns

---

## 🆘 Getting Help

- **GitHub Issues**: [Report bugs](https://github.com/your-username/consistly/issues)
- **Discussions**: [Community support](https://github.com/your-username/consistly/discussions)  
- **Email**: ashutosh@yourcompany.com

---

## ✅ Success Checklist

- [ ] Ollama installed and running
- [ ] AI model downloaded  
- [ ] Consistly cloned and dependencies installed
- [ ] App running on http://localhost:8000
- [ ] Successfully processed test content
- [ ] Verified no external network calls

**🎯 You're all set! Your content is now processed with complete privacy.**
