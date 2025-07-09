"""
File Processing Module

Handles extraction of text content from various file formats
including PDF, DOCX, and TXT files.
"""

import os
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from typing import Union, BinaryIO

import PyPDF2
from docx import Document
from fastapi import HTTPException, UploadFile


class FileProcessor:
    """
    Handles file processing and text extraction from multiple formats.
    
    Supported formats:
    - PDF (.pdf)
    - Microsoft Word (.docx)
    - Plain text (.txt)
    """
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    def __init__(self):
        """Initialize the file processor."""
        pass
    
    async def extract_text_from_upload(self, file: UploadFile) -> str:
        """
        Extract text content from an uploaded file.
        
        Args:
            file (UploadFile): The uploaded file object
            
        Returns:
            str: Extracted text content
            
        Raises:
            HTTPException: If file processing fails
        """
        if not self._is_valid_file(file):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp_file:
            content = await file.read()
            
            if len(content) > self.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Maximum size: {self.MAX_FILE_SIZE // (1024*1024)}MB"
                )
            
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            return self._extract_text_by_extension(tmp_file_path, file.filename)
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    def _is_valid_file(self, file: UploadFile) -> bool:
        """
        Check if the uploaded file has a supported extension.
        
        Args:
            file (UploadFile): The uploaded file object
            
        Returns:
            bool: True if file extension is supported
        """
        if not file.filename:
            return False
        
        extension = os.path.splitext(file.filename.lower())[1]
        return extension in self.SUPPORTED_EXTENSIONS
    
    def _extract_text_by_extension(self, file_path: str, filename: str) -> str:
        """
        Extract text based on file extension.
        
        Args:
            file_path (str): Path to the temporary file
            filename (str): Original filename
            
        Returns:
            str: Extracted text content
        """
        extension = os.path.splitext(filename.lower())[1]
        
        if extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif extension == '.docx':
            return self._extract_from_docx(file_path)
        else:  # .txt
            return self._extract_from_txt(file_path)
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF file.
        
        Args:
            file_path (str): Path to PDF file
            
        Returns:
            str: Extracted text content
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_parts = []
                
                for page in pdf_reader.pages:
                    text_parts.append(page.extract_text())
                
                return '\n'.join(text_parts)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to extract text from PDF: {str(e)}"
            )
    
    def _extract_from_docx(self, file_path: str) -> str:
        """
        Extract text from DOCX file.
        
        Args:
            file_path (str): Path to DOCX file
            
        Returns:
            str: Extracted text content
        """
        try:
            # Primary method using python-docx
            doc = Document(file_path)
            text_parts = [paragraph.text for paragraph in doc.paragraphs]
            return '\n'.join(text_parts)
        except Exception:
            # Fallback method using XML extraction
            try:
                return self._extract_docx_fallback(file_path)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to extract text from DOCX: {str(e)}"
                )
    
    def _extract_docx_fallback(self, file_path: str) -> str:
        """
        Fallback method to extract text from DOCX using XML parsing.
        
        Args:
            file_path (str): Path to DOCX file
            
        Returns:
            str: Extracted text content
        """
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            xml_content = zip_file.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            text_parts = []
            for elem in root.iter():
                if elem.text:
                    text_parts.append(elem.text)
            
            return ' '.join(text_parts)
    
    def _extract_from_txt(self, file_path: str) -> str:
        """
        Extract text from TXT file.
        
        Args:
            file_path (str): Path to TXT file
            
        Returns:
            str: File content as string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to read text file: {str(e)}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to read text file: {str(e)}"
            )