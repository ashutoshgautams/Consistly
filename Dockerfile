FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create optimized startup script
RUN cat > start.sh << 'SCRIPT'
#!/bin/bash
set -e

echo "🚀 Starting Consistly on Railway..."

# Start Ollama in background
echo "🤖 Starting Ollama..."
ollama serve &

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama..."
for i in $(seq 1 30); do
    if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
        echo "✅ Ollama is ready!"
        break
    fi
    echo "⏳ Attempt $i/30..."
    sleep 2
done

# Download model (Railway has good bandwidth)
echo "📥 Downloading AI model..."
if ! ollama list | grep -q "llama3.1:8b"; then
    echo "📥 First-time setup: downloading model (~5 minutes)..."
    ollama pull llama3.1:8b
    echo "✅ Model downloaded successfully!"
else
    echo "✅ Model already available!"
fi

# Start the web server
echo "🌐 Starting Consistly web server..."
exec uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info
SCRIPT

RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
