#!/bin/bash
set -e

echo "🚀 Starting Consistly on Railway..."

# Start Ollama in background with proper process management
echo "🤖 Starting Ollama..."
ollama serve &
OLLAMA_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down..."
    kill $OLLAMA_PID 2>/dev/null || true
    exit
}

# Set trap for cleanup
trap cleanup SIGTERM SIGINT

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama..."
for i in $(seq 1 30); do
    if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
        echo "✅ Ollama is ready!"
        break
    fi
    echo "⏳ Attempt $i/30..."
    sleep 3
done

# Check if Ollama is actually ready
if ! curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "❌ Ollama failed to start properly"
    exit 1
fi

# Download model in background to avoid blocking
echo "📥 Checking for AI model..."
(
    if ! ollama list | grep -q "llama3.1:8b"; then
        echo "📥 Downloading model in background..."
        ollama pull llama3.1:8b
        echo "✅ Model ready!"
    else
        echo "✅ Model already available!"
    fi
) &

# Start the web server (keep Ollama running)
echo "🌐 Starting Consistly web server on port $PORT..."
uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info &
WEB_PID=$!

# Wait for either process to exit
wait $WEB_PID
