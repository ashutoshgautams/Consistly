"""
AI Engine Module

Handles communication with Ollama and manages AI-powered
text analysis and editing processes.
"""

import requests
from typing import List, Dict, Any
from fastapi import HTTPException


class AIEngine:
    """
    Manages AI operations for style analysis and content editing.
    
    This class handles communication with the Ollama API and provides
    high-level methods for style analysis and content improvement.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3:8b"):
        """
        Initialize the AI engine.
        
        Args:
            base_url (str): Ollama server base URL
            model (str): Model name to use for generation
        """
        self.base_url = base_url
        self.model = model
        self.generate_url = f"{base_url}/api/generate"
        self.health_url = f"{base_url}/"
        
        # Generation parameters
        self.generation_params = {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 2000
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check if Ollama service is available and working.
        
        Returns:
            Dict[str, Any]: Health check results
        """
        try:
            # Check if Ollama is running
            health_response = requests.get(self.health_url, timeout=5)
            if health_response.status_code != 200:
                return {
                    "status": "error",
                    "message": "Ollama server not responding",
                    "details": f"HTTP {health_response.status_code}"
                }
            
            # Test model generation
            test_response = await self._generate_text("Say hello in one sentence.")
            return {
                "status": "success",
                "message": "AI engine is operational",
                "test_output": test_response[:100] + "..." if len(test_response) > 100 else test_response
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "details": "Failed to connect to AI service"
            }
    
    async def analyze_writing_style(self, reference_articles: List[str]) -> str:
        """
        Analyze writing style from reference articles.
        
        Args:
            reference_articles (List[str]): List of reference article texts
            
        Returns:
            str: Style analysis and guide
        """
        if not reference_articles:
            raise HTTPException(status_code=400, detail="No reference articles provided")
        
        prompt = self._create_style_analysis_prompt(reference_articles)
        return await self._generate_text(prompt)
    
    async def edit_content(self, draft_content: str, style_guide: str) -> str:
        """
        Edit content according to the provided style guide.
        
        Args:
            draft_content (str): Original draft content
            style_guide (str): Style guide from analysis
            
        Returns:
            str: Edited content
        """
        if not draft_content or not style_guide:
            raise HTTPException(status_code=400, detail="Missing content or style guide")
        
        prompt = self._create_editing_prompt(draft_content, style_guide)
        return await self._generate_text(prompt)
    
    async def process_complete_workflow(self, reference_articles: List[str], draft_content: str) -> str:
        """
        Complete workflow: analyze style and edit content.
        
        Args:
            reference_articles (List[str]): Reference articles for style analysis
            draft_content (str): Draft content to edit
            
        Returns:
            str: Final edited content
        """
        # Step 1: Analyze writing style
        style_guide = await self.analyze_writing_style(reference_articles)
        
        # Step 2: Edit content using style guide
        edited_content = await self.edit_content(draft_content, style_guide)
        
        return edited_content
    
    async def _generate_text(self, prompt: str) -> str:
        """
        Generate text using Ollama API.
        
        Args:
            prompt (str): Input prompt for generation
            
        Returns:
            str: Generated text response
        """
        try:
            response = requests.post(
                self.generate_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": self.generation_params
                },
                timeout=120  # 2 minute timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                error_detail = f"AI API error: {response.status_code} - {response.text}"
                raise HTTPException(status_code=500, detail=error_detail)
                
        except requests.exceptions.Timeout:
            raise HTTPException(status_code=500, detail="AI request timed out")
        except requests.exceptions.ConnectionError:
            raise HTTPException(
                status_code=500,
                detail="Could not connect to AI service. Make sure Ollama is running."
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI processing error: {str(e)}")
    
    def _create_style_analysis_prompt(self, reference_articles: List[str]) -> str:
        """
        Create a prompt for style analysis.
        
        Args:
            reference_articles (List[str]): Reference articles
            
        Returns:
            str: Formatted prompt for style analysis
        """
        articles_text = "\n\n---ARTICLE SEPARATOR---\n\n".join(reference_articles)
        
        return f"""
You are an expert writing style analyst. Analyze the following articles and create a comprehensive style guide.

REFERENCE ARTICLES:
{articles_text}

Please provide a detailed analysis covering:

1. TONE & VOICE CHARACTERISTICS:
   - Overall tone (professional, casual, authoritative, etc.)
   - Voice personality traits
   - Emotional undertones

2. STRUCTURAL PATTERNS:
   - Typical opening strategies
   - Paragraph organization and flow
   - Conclusion styles
   - Use of headings and subheadings

3. LANGUAGE PREFERENCES:
   - Vocabulary sophistication level
   - Industry jargon vs. accessible language
   - Sentence length and complexity
   - Active vs. passive voice usage

4. CONTENT APPROACH:
   - How examples and evidence are presented
   - Use of statistics, quotes, or case studies
   - Storytelling elements
   - Call-to-action styles

5. DISTINCTIVE ELEMENTS:
   - Unique phrases or expressions
   - Formatting preferences
   - Brand voice indicators

Create a concise but comprehensive style guide that can be used to edit future content to match this writing style.
"""
    
    def _create_editing_prompt(self, draft_content: str, style_guide: str) -> str:
        """
        Create a prompt for content editing.
        
        Args:
            draft_content (str): Original draft
            style_guide (str): Style guide from analysis
            
        Returns:
            str: Formatted prompt for content editing
        """
        return f"""
You are an expert content editor. Your task is to edit the following draft to match the provided style guide exactly.

STYLE GUIDE TO FOLLOW:
{style_guide}

DRAFT TO EDIT:
{draft_content}

EDITING INSTRUCTIONS:
1. Maintain the core message and key information from the original draft
2. Adjust tone, voice, and style to match the style guide
3. Improve sentence structure and flow according to the patterns identified
4. Enhance vocabulary and word choice to align with the reference style
5. Reorganize content structure if needed to match the typical patterns
6. Add or modify examples to fit the content approach described in the style guide
7. Ensure the final piece feels authentic to the original brand voice

Please provide only the edited version of the article. Do not include explanations or commentary about the changes made.
"""