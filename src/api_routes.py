"""
API Routes Module

Defines all API endpoints for the application including
file upload, text processing, and AI generation routes.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from .file_processor import FileProcessor
from .ai_engine import AIEngine


class GenerateEditRequest(BaseModel):
    """Request model for content generation."""
    reference_articles: List[str]
    draft_content: str


class APIResponse(BaseModel):
    """Standard API response model."""
    success: bool
    data: Dict[str, Any] = {}
    message: str = ""


def create_api_routes(file_processor: FileProcessor, ai_engine: AIEngine) -> APIRouter:
    """
    Create and configure API routes.
    
    Args:
        file_processor (FileProcessor): File processing instance
        ai_engine (AIEngine): AI engine instance
        
    Returns:
        APIRouter: Configured API router
    """
    router = APIRouter(prefix="/api", tags=["API"])
    
    @router.get("/health")
    async def health_check():
        """
        Check overall system health including AI service.
        
        Returns:
            Dict: Health status information
        """
        ai_health = await ai_engine.health_check()
        
        return {
            "status": "healthy",
            "version": "2.0.0",
            "ai_service": ai_health,
            "supported_formats": list(file_processor.SUPPORTED_EXTENSIONS)
        }
    
    @router.post("/extract-text")
    async def extract_text_from_file(file: UploadFile = File(...)):
        """
        Extract text content from uploaded file.
        
        Args:
            file (UploadFile): Uploaded file
            
        Returns:
            Dict: Extracted text content
        """
        try:
            text = await file_processor.extract_text_from_upload(file)
            return APIResponse(
                success=True,
                data={"text": text, "filename": file.filename},
                message="Text extracted successfully"
            ).dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")
    
    @router.post("/analyze-style")
    async def analyze_writing_style(request: Dict[str, List[str]]):
        """
        Analyze writing style from reference articles.
        
        Args:
            request: Dictionary containing reference_articles list
            
        Returns:
            Dict: Style analysis results
        """
        try:
            reference_articles = request.get("reference_articles", [])
            if not reference_articles:
                raise HTTPException(status_code=400, detail="No reference articles provided")
            
            style_guide = await ai_engine.analyze_writing_style(reference_articles)
            
            return APIResponse(
                success=True,
                data={"style_guide": style_guide},
                message="Style analysis completed"
            ).dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Style analysis failed: {str(e)}")
    
    @router.post("/edit-content")
    async def edit_content(request: Dict[str, str]):
        """
        Edit content according to provided style guide.
        
        Args:
            request: Dictionary containing draft_content and style_guide
            
        Returns:
            Dict: Edited content
        """
        try:
            draft_content = request.get("draft_content", "")
            style_guide = request.get("style_guide", "")
            
            if not draft_content or not style_guide:
                raise HTTPException(status_code=400, detail="Missing content or style guide")
            
            edited_content = await ai_engine.edit_content(draft_content, style_guide)
            
            return APIResponse(
                success=True,
                data={"edited_content": edited_content},
                message="Content editing completed"
            ).dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Content editing failed: {str(e)}")
    
    @router.post("/generate-edit")
    async def generate_complete_edit(request: GenerateEditRequest):
        """
        Complete workflow: analyze style and edit content.
        
        Args:
            request (GenerateEditRequest): Request with reference articles and draft
            
        Returns:
            Dict: Final edited article
        """
        try:
            if not request.reference_articles:
                raise HTTPException(status_code=400, detail="No reference articles provided")
            
            if not request.draft_content.strip():
                raise HTTPException(status_code=400, detail="No draft content provided")
            
            # Process complete workflow
            edited_article = await ai_engine.process_complete_workflow(
                request.reference_articles,
                request.draft_content
            )
            
            return APIResponse(
                success=True,
                data={"edited_article": edited_article},
                message="Article editing completed successfully"
            ).dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Article generation failed: {str(e)}")
    
    @router.get("/models")
    async def get_available_models():
        """
        Get information about available AI models.
        
        Returns:
            Dict: Available models and current configuration
        """
        return {
            "current_model": ai_engine.model,
            "base_url": ai_engine.base_url,
            "generation_params": ai_engine.generation_params,
            "status": "operational"
        }
    
    return router