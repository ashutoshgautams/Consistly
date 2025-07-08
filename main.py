"""
AI Writing Style Copier - Main Application

A sophisticated AI-powered tool that learns from your existing content
to automatically edit and improve new drafts, maintaining consistent
brand voice and writing style.

Author: Ashutosh Gautam
GitHub: https://github.com/your-username/ai-writing-style-copier
"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.file_processor import FileProcessor
from src.ai_engine import AIEngine
from src.api_routes import create_api_routes
from src.ui_components import UIRenderer

# Application metadata
APP_NAME = "AI Writing Style Copier"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Transform your drafts to match your brand's unique voice"

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        description=APP_DESCRIPTION,
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize components
    file_processor = FileProcessor()
    ai_engine = AIEngine()
    ui_renderer = UIRenderer()
    
    # Create API routes
    api_router = create_api_routes(file_processor, ai_engine)
    app.include_router(api_router)
    
    # Serve main UI
    @app.get("/", response_class=HTMLResponse)
    async def serve_ui():
        """Serve the main user interface."""
        return ui_renderer.render_main_page()
    
    return app

# Create application instance
app = create_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
    