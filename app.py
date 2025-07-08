import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import requests
import json
from typing import List
import tempfile
from docx import Document
import zipfile
import xml.etree.ElementTree as ET
import PyPDF2
import io

app = FastAPI(title="AI Writing Style Copier", version="2.0.0")

# Enable CORS for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

def call_ollama(prompt: str, model: str = "llama3:8b"):
    """Call Ollama API to generate text"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 2000
                }
            },
            timeout=120  # 2 minute timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            error_detail = f"Ollama API error: {response.status_code} - {response.text}"
            print(f"Ollama error: {error_detail}")
            raise HTTPException(status_code=500, detail=error_detail)
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=500, detail="Ollama request timed out")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Could not connect to Ollama. Make sure 'ollama serve' is running.")
    except Exception as e:
        error_msg = f"Error calling Ollama: {str(e)}"
        print(f"Ollama error: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    except Exception:
        # Fallback: Extract from XML
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                xml_content = zip_file.read('word/document.xml')
                root = ET.fromstring(xml_content)
                
                # Extract text from XML
                text = []
                for elem in root.iter():
                    if elem.text:
                        text.append(elem.text)
                return ' '.join(text)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not extract text from document: {str(e)}")

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = []
            for page in pdf_reader.pages:
                text.append(page.extract_text())
            return '\n'.join(text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not extract text from PDF: {str(e)}")

def create_style_analysis_prompt(reference_articles: List[str]) -> str:
    """Create a prompt to analyze writing style from reference articles"""
    articles_text = "\n\n---ARTICLE SEPARATOR---\n\n".join(reference_articles)
    
    return f"""
Analyze the following articles and identify the key writing style patterns, tone, structure, and standards:

{articles_text}

Please identify:
1. Tone and voice characteristics
2. Sentence structure patterns
3. Paragraph organization
4. Word choice preferences
5. Common phrases or expressions
6. Overall writing standards and quality markers

Provide a concise style guide that can be used to edit future articles.
"""

def create_editing_prompt(draft_content: str, style_guide: str) -> str:
    """Create a prompt to edit the draft according to the style guide"""
    return f"""
You are an expert editor. Use the following style guide to edit and improve the draft article:

STYLE GUIDE:
{style_guide}

DRAFT TO EDIT:
{draft_content}

Please edit the draft to match the style guide. Make improvements to:
- Tone and voice consistency
- Sentence structure and flow
- Word choice and vocabulary
- Paragraph organization
- Overall clarity and quality

Return only the edited version of the article, maintaining the same general structure but improving it according to the style guide.
"""

@app.get("/test-ollama")
async def test_ollama():
    """Test if Ollama is working"""
    try:
        # First check if Ollama is running
        health_response = requests.get("http://localhost:11434/", timeout=5)
        if health_response.status_code != 200:
            return {"status": "error", "message": "Ollama server not responding"}
        
        # Test a simple generation
        test_response = call_ollama("Say hello in one sentence.", "llama3:8b")
        return {"status": "success", "message": "Ollama is working", "test_output": test_response}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    """Serve the frontend HTML"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Writing Style Copier</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #fef7f0 0%, #fdf2e9 50%, #fef7f0 100%);
                min-height: 100vh;
                color: #333;
                line-height: 1.6;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
                padding: 40px 0;
            }
            
            .header h1 {
                font-size: 3rem;
                font-weight: 800;
                color: #e6533a;
                margin-bottom: 10px;
                text-shadow: 0 2px 4px rgba(230, 83, 58, 0.1);
            }
            
            .header p {
                font-size: 1.2rem;
                color: #666;
                font-weight: 300;
            }
            
            .main-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }
            
            .card {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(230, 83, 58, 0.1);
                border: 1px solid rgba(230, 83, 58, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(230, 83, 58, 0.15);
            }
            
            .card h2 {
                color: #e6533a;
                font-size: 1.5rem;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .card h2 i {
                font-size: 1.2rem;
            }
            
            .input-group {
                margin-bottom: 20px;
            }
            
            .input-group label {
                display: block;
                margin-bottom: 8px;
                color: #e6533a;
                font-weight: 600;
                font-size: 0.9rem;
            }
            
            .file-upload {
                position: relative;
                display: inline-block;
                width: 100%;
            }
            
            .file-upload input[type="file"] {
                position: absolute;
                opacity: 0;
                width: 100%;
                height: 100%;
                cursor: pointer;
            }
            
            .file-upload-label {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                padding: 15px 20px;
                background: linear-gradient(135deg, #e6533a, #ff6b47);
                color: white;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 600;
                border: none;
                width: 100%;
            }
            
            .file-upload-label:hover {
                background: linear-gradient(135deg, #d64c36, #e6533a);
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(230, 83, 58, 0.3);
            }
            
            .textarea-input {
                width: 100%;
                min-height: 120px;
                padding: 15px;
                border: 2px solid rgba(230, 83, 58, 0.2);
                border-radius: 12px;
                font-family: inherit;
                font-size: 14px;
                background: rgba(255, 255, 255, 0.8);
                resize: vertical;
                transition: border-color 0.3s ease, box-shadow 0.3s ease;
            }
            
            .textarea-input:focus {
                outline: none;
                border-color: #e6533a;
                box-shadow: 0 0 0 3px rgba(230, 83, 58, 0.1);
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #e6533a, #ff6b47);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 12px;
                cursor: pointer;
                font-weight: 600;
                font-size: 14px;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                justify-content: center;
                min-width: 120px;
            }
            
            .btn-primary:hover {
                background: linear-gradient(135deg, #d64c36, #e6533a);
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(230, 83, 58, 0.3);
            }
            
            .btn-secondary {
                background: rgba(230, 83, 58, 0.1);
                color: #e6533a;
                border: 2px solid rgba(230, 83, 58, 0.2);
                padding: 8px 16px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                font-size: 12px;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 6px;
            }
            
            .btn-secondary:hover {
                background: rgba(230, 83, 58, 0.2);
                border-color: #e6533a;
            }
            
            .status {
                padding: 10px 15px;
                border-radius: 8px;
                margin-top: 10px;
                font-size: 14px;
                font-weight: 500;
            }
            
            .status.success {
                background: rgba(34, 197, 94, 0.1);
                color: #059669;
                border: 1px solid rgba(34, 197, 94, 0.2);
            }
            
            .status.error {
                background: rgba(239, 68, 68, 0.1);
                color: #dc2626;
                border: 1px solid rgba(239, 68, 68, 0.2);
            }
            
            .reference-item {
                margin-bottom: 15px;
                padding: 15px;
                background: rgba(230, 83, 58, 0.05);
                border-radius: 10px;
                border: 1px solid rgba(230, 83, 58, 0.1);
            }
            
            .add-reference {
                margin-top: 10px;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
                color: #e6533a;
                font-weight: 600;
            }
            
            .loading i {
                animation: spin 1s linear infinite;
                margin-right: 10px;
            }
            
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            .output-section {
                grid-column: 1 / -1;
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(230, 83, 58, 0.1);
                border: 1px solid rgba(230, 83, 58, 0.1);
            }
            
            .output-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            
            .output-textarea {
                width: 100%;
                min-height: 300px;
                padding: 20px;
                border: 2px solid rgba(230, 83, 58, 0.2);
                border-radius: 12px;
                font-family: inherit;
                font-size: 15px;
                line-height: 1.6;
                background: rgba(255, 255, 255, 0.8);
                resize: vertical;
            }
            
            .copy-btn {
                position: relative;
            }
            
            .copy-success {
                position: absolute;
                top: -30px;
                right: 0;
                background: #059669;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .copy-success.show {
                opacity: 1;
            }
            
            .generate-section {
                text-align: center;
                margin: 30px 0;
            }
            
            .generate-btn {
                background: linear-gradient(135deg, #e6533a, #ff6b47);
                color: white;
                border: none;
                padding: 20px 40px;
                border-radius: 16px;
                cursor: pointer;
                font-weight: 700;
                font-size: 18px;
                transition: all 0.3s ease;
                display: inline-flex;
                align-items: center;
                gap: 12px;
                box-shadow: 0 4px 20px rgba(230, 83, 58, 0.3);
            }
            
            .generate-btn:hover {
                background: linear-gradient(135deg, #d64c36, #e6533a);
                transform: translateY(-3px);
                box-shadow: 0 8px 30px rgba(230, 83, 58, 0.4);
            }
            
            .generate-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            @media (max-width: 768px) {
                .main-grid {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 2rem;
                }
                
                .container {
                    padding: 15px;
                }
                
                .card {
                    padding: 20px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-magic"></i> AI Writing Style Copier</h1>
                <p>Transform your drafts to match your brand's unique voice and style</p>
            </div>
            
            <div class="main-grid">
                <!-- Reference Articles Section -->
                <div class="card">
                    <h2><i class="fas fa-book"></i> Reference Articles</h2>
                    <p style="color: #666; margin-bottom: 20px; font-size: 14px;">
                        Upload or paste 3-5 articles that represent your writing style
                    </p>
                    
                    <div id="referenceContainer">
                        <div class="reference-item">
                            <div class="input-group">
                                <label>Reference Article 1</label>
                                <div class="file-upload">
                                    <input type="file" id="refFile1" accept=".txt,.docx,.pdf">
                                    <div class="file-upload-label">
                                        <i class="fas fa-upload"></i>
                                        Upload File (.txt, .docx, .pdf)
                                    </div>
                                </div>
                                <div style="margin: 10px 0; text-align: center; color: #666; font-size: 14px;">or</div>
                                <textarea class="textarea-input" id="refText1" placeholder="Paste your reference article here..."></textarea>
                            </div>
                        </div>
                    </div>
                    
                    <button class="btn-secondary add-reference" onclick="addReferenceField()">
                        <i class="fas fa-plus"></i> Add Another Reference
                    </button>
                    
                    <div id="referenceStatus"></div>
                </div>
                
                <!-- Draft Article Section -->
                <div class="card">
                    <h2><i class="fas fa-edit"></i> Draft Article</h2>
                    <p style="color: #666; margin-bottom: 20px; font-size: 14px;">
                        Upload or paste the draft article you want to improve
                    </p>
                    
                    <div class="input-group">
                        <label>Draft Article</label>
                        <div class="file-upload">
                            <input type="file" id="draftFile" accept=".txt,.docx,.pdf">
                            <div class="file-upload-label">
                                <i class="fas fa-upload"></i>
                                Upload File (.txt, .docx, .pdf)
                            </div>
                        </div>
                        <div style="margin: 10px 0; text-align: center; color: #666; font-size: 14px;">or</div>
                        <textarea class="textarea-input" id="draftText" placeholder="Paste your draft article here..." style="min-height: 200px;"></textarea>
                    </div>
                    
                    <div id="draftStatus"></div>
                </div>
            </div>
            
            <!-- Generate Section -->
            <div class="generate-section">
                <button class="generate-btn" onclick="generateEdit()" id="generateBtn">
                    <i class="fas fa-wand-magic-sparkles"></i>
                    Generate Edited Article
                </button>
                
                <div class="loading" id="loading">
                    <i class="fas fa-spinner"></i>
                    Processing your article... This may take a minute.
                </div>
            </div>
            
            <!-- Output Section -->
            <div class="output-section">
                <div class="output-header">
                    <h2><i class="fas fa-sparkles"></i> Edited Article</h2>
                    <button class="btn-primary copy-btn" onclick="copyToClipboard()" id="copyBtn">
                        <i class="fas fa-copy"></i>
                        Copy
                        <div class="copy-success" id="copySuccess">Copied!</div>
                    </button>
                </div>
                <textarea class="output-textarea" id="result" placeholder="Your beautifully edited article will appear here..." readonly></textarea>
            </div>
        </div>

        <script>
            let referenceCount = 1;
            let referenceTexts = [];
            let draftContent = '';

            // File upload handlers
            document.addEventListener('change', function(e) {
                if (e.target.type === 'file') {
                    handleFileUpload(e.target);
                }
            });

            // Text area handlers
            document.addEventListener('input', function(e) {
                if (e.target.classList.contains('textarea-input')) {
                    if (e.target.id === 'draftText') {
                        draftContent = e.target.value;
                        updateDraftStatus();
                    } else if (e.target.id.startsWith('refText')) {
                        updateReferenceStatus();
                    }
                }
            });

            async function handleFileUpload(fileInput) {
                const file = fileInput.files[0];
                if (!file) return;

                const formData = new FormData();
                formData.append('file', file);

                try {
                    const response = await fetch('/extract-text', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        throw new Error('Failed to extract text from file');
                    }
                    
                    const data = await response.json();
                    
                    if (fileInput.id === 'draftFile') {
                        document.getElementById('draftText').value = data.text;
                        draftContent = data.text;
                        updateDraftStatus();
                    } else if (fileInput.id.startsWith('refFile')) {
                        const refNum = fileInput.id.replace('refFile', '');
                        document.getElementById(`refText${refNum}`).value = data.text;
                        updateReferenceStatus();
                    }
                } catch (error) {
                    showError(fileInput.id.includes('draft') ? 'draftStatus' : 'referenceStatus', 
                             `Error processing file: ${error.message}`);
                }
            }

            function addReferenceField() {
                referenceCount++;
                const container = document.getElementById('referenceContainer');
                
                const newReference = document.createElement('div');
                newReference.className = 'reference-item';
                newReference.innerHTML = `
                    <div class="input-group">
                        <label>Reference Article ${referenceCount}</label>
                        <div class="file-upload">
                            <input type="file" id="refFile${referenceCount}" accept=".txt,.docx,.pdf">
                            <div class="file-upload-label">
                                <i class="fas fa-upload"></i>
                                Upload File (.txt, .docx, .pdf)
                            </div>
                        </div>
                        <div style="margin: 10px 0; text-align: center; color: #666; font-size: 14px;">or</div>
                        <textarea class="textarea-input" id="refText${referenceCount}" placeholder="Paste your reference article here..."></textarea>
                        <button class="btn-secondary" onclick="removeReference(this)" style="margin-top: 10px;">
                            <i class="fas fa-trash"></i> Remove
                        </button>
                    </div>
                `;
                
                container.appendChild(newReference);
            }

            function removeReference(button) {
                button.closest('.reference-item').remove();
                updateReferenceStatus();
            }

            function updateReferenceStatus() {
                referenceTexts = [];
                for (let i = 1; i <= referenceCount; i++) {
                    const textArea = document.getElementById(`refText${i}`);
                    if (textArea && textArea.value.trim()) {
                        referenceTexts.push(textArea.value.trim());
                    }
                }
                
                const statusDiv = document.getElementById('referenceStatus');
                if (referenceTexts.length > 0) {
                    statusDiv.innerHTML = `<div class="status success">
                        <i class="fas fa-check"></i> ${referenceTexts.length} reference article(s) ready
                    </div>`;
                } else {
                    statusDiv.innerHTML = '';
                }
            }

            function updateDraftStatus() {
                const statusDiv = document.getElementById('draftStatus');
                if (draftContent.trim()) {
                    statusDiv.innerHTML = `<div class="status success">
                        <i class="fas fa-check"></i> Draft article ready
                    </div>`;
                } else {
                    statusDiv.innerHTML = '';
                }
            }

            function showError(elementId, message) {
                document.getElementById(elementId).innerHTML = `<div class="status error">
                    <i class="fas fa-exclamation-triangle"></i> ${message}
                </div>`;
            }

            async function generateEdit() {
                // Collect all reference texts
                updateReferenceStatus();
                draftContent = document.getElementById('draftText').value.trim();
                
                if (referenceTexts.length === 0) {
                    showError('referenceStatus', 'Please add at least one reference article');
                    return;
                }
                
                if (!draftContent) {
                    showError('draftStatus', 'Please add your draft article');
                    return;
                }

                const generateBtn = document.getElementById('generateBtn');
                const loading = document.getElementById('loading');
                const resultTextarea = document.getElementById('result');
                
                generateBtn.disabled = true;
                loading.style.display = 'block';
                resultTextarea.value = '';

                try {
                    const response = await fetch('/generate-edit', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            reference_articles: referenceTexts,
                            draft_content: draftContent
                        })
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || `HTTP ${response.status}`);
                    }
                    
                    const data = await response.json();
                    resultTextarea.value = data.edited_article;
                    
                    // Scroll to results
                    resultTextarea.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    
                } catch (error) {
                    console.error('Error:', error);
                    resultTextarea.value = `Error: ${error.message}`;
                } finally {
                    generateBtn.disabled = false;
                    loading.style.display = 'none';
                }
            }

            async function copyToClipboard() {
                const textarea = document.getElementById('result');
                const copySuccess = document.getElementById('copySuccess');
                
                try {
                    await navigator.clipboard.writeText(textarea.value);
                    copySuccess.classList.add('show');
                    setTimeout(() => {
                        copySuccess.classList.remove('show');
                    }, 2000);
                } catch (err) {
                    // Fallback for older browsers
                    textarea.select();
                    document.execCommand('copy');
                    copySuccess.classList.add('show');
                    setTimeout(() => {
                        copySuccess.classList.remove('show');
                    }, 2000);
                }
            }

            // Initialize
            updateReferenceStatus();
            updateDraftStatus();
        </script>
    </body>
    </html>
    """

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """Extract text from uploaded file"""
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        if file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(tmp_file_path)
        elif file.filename.lower().endswith('.docx'):
            text = extract_text_from_docx(tmp_file_path)
        else:
            # Assume it's a text file
            text = content.decode('utf-8')
        
        return {"text": text}
    finally:
        os.unlink(tmp_file_path)

@app.post("/generate-edit")
async def generate_edit(request: dict):
    """Generate edited article using AI"""
    reference_articles = request.get("reference_articles", [])
    draft_content = request.get("draft_content", "")
    
    if not reference_articles or not draft_content:
        raise HTTPException(status_code=400, detail="Missing reference articles or draft content")
    
    # Step 1: Analyze writing style from reference articles
    style_prompt = create_style_analysis_prompt(reference_articles)
    style_guide = call_ollama(style_prompt)
    
    # Step 2: Edit the draft using the style guide
    edit_prompt = create_editing_prompt(draft_content, style_guide)
    edited_article = call_ollama(edit_prompt)
    
    return {"edited_article": edited_article}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)