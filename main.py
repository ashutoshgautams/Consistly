from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests
import os
import logging
from ui_components import UIRenderer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Consistly", description="Style-Consistent Content Generation")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1:8b"
PORT = int(os.getenv("PORT", 8000))

class EditRequest(BaseModel):
    reference_articles: List[str]
    draft_content: str

class EditResponse(BaseModel):
    data: dict

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main application page"""
    try:
        renderer = UIRenderer()
        return renderer.render_main_page()
    except Exception as e:
        logger.error(f"Error rendering main page: {e}")
        return HTMLResponse("<h1>Consistly - Loading...</h1>")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/version", timeout=5)
        if response.status_code == 200:
            # Check if model is available
            models_response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
            models = models_response.json().get("models", [])
            model_available = any(OLLAMA_MODEL in model.get("name", "") for model in models)
            
            return {
                "status": "healthy" if model_available else "loading",
                "ai_service": {
                    "status": "success" if model_available else "downloading",
                    "message": f"Ollama ready with {OLLAMA_MODEL}" if model_available else "AI model downloading..."
                }
            }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
    
    return {
        "status": "starting",
        "ai_service": {
            "status": "loading",
            "message": "AI service is starting up (first time takes ~5 minutes)..."
        }
    }

@app.post("/api/generate-edit", response_model=EditResponse)
async def generate_edit(request: EditRequest):
    """Generate style-consistent content"""
    try:
        logger.info(f"Processing request with {len(request.reference_articles)} references")
        
        # Validate input
        if not request.reference_articles:
            raise HTTPException(status_code=400, detail="Please provide at least one reference article")
        
        if not request.draft_content.strip():
            raise HTTPException(status_code=400, detail="Draft content cannot be empty")
        
        # Check if Ollama is ready
        if not await check_ollama_ready():
            raise HTTPException(
                status_code=503, 
                detail="AI service is still starting up. Please wait a moment and try again."
            )
        
        # Generate content
        result = await generate_with_ollama(request)
        
        logger.info("Content generation completed successfully")
        return EditResponse(data={"edited_article": result})
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

async def check_ollama_ready():
    """Check if Ollama is ready and model is available"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/version", timeout=5)
        if response.status_code != 200:
            return False
        
        models_response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if models_response.status_code != 200:
            return False
            
        models = models_response.json().get("models", [])
        return any(OLLAMA_MODEL in model.get("name", "") for model in models)
    
    except Exception:
        return False

async def generate_with_ollama(request: EditRequest):
    """Generate content using Ollama"""
    
    # Combine reference articles
    references = "\n\n---\n\n".join(request.reference_articles)
    
    prompt = f"""You are a professional content editor. Transform the draft to match the writing style of the reference content.

REFERENCE CONTENT:
{references}

DRAFT TO TRANSFORM:
{request.draft_content}

Transform the draft to match the style, tone, vocabulary, and structure of the reference content while preserving the original meaning. Provide only the transformed content:"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 2000
        }
    }
    
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            raise Exception(f"AI service error: {response.status_code}")
        
        result = response.json()
        generated_text = result.get("response", "").strip()
        
        if not generated_text:
            raise Exception("AI service returned empty response")
        
        return generated_text
    
    except requests.exceptions.Timeout:
        raise Exception("Request timed out. Try with shorter content.")
    except Exception as e:
        raise Exception(f"Generation failed: {str(e)}")

@app.post("/api/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """Extract text from uploaded files"""
    try:
        logger.info(f"Extracting text from: {file.filename}")
        
        if file.size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
        
        content = await file.read()
        
        if file.filename.endswith('.txt'):
            text = content.decode('utf-8')
        elif file.filename.endswith('.docx'):
            from docx import Document
            import io
            doc = Document(io.BytesIO(content))
            text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
        else:
            raise HTTPException(status_code=400, detail="Only .txt and .docx files supported")
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="File appears to be empty")
        
        return {"data": {"text": text}}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
