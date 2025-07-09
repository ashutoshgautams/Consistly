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

# Download model
echo "📥 Downloading AI model..."
if ! ollama list | grep -q "llama3.1:8b"; then
    echo "📥 First-time setup: downloading model..."
    ollama pull llama3.1:8b
    echo "✅ Model downloaded!"
else
    echo "✅ Model already available!"
fi

# Start the web server
echo "🌐 Starting Consistly web server on port $PORT..."
exec uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info
