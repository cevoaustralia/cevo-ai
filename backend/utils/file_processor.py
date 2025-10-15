import base64
import re
from enum import Enum
from typing import Dict, List, Optional, Any
from fastapi import UploadFile, HTTPException

# Constants
MAX_IMAGE_SIZE = 3.75 * 1024 * 1024  # 3.75 MB
MAX_DOCUMENT_SIZE = 4.5 * 1024 * 1024  # 4.5 MB
MAX_IMAGES = 20
MAX_DOCUMENTS = 5

class ContentType(Enum):
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_GIF = "image/gif"
    IMAGE_WEBP = "image/webp"
    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    CSV = "text/csv"
    TXT = "text/plain"
    HTML = "text/html"
    MARKDOWN = "text/markdown"

class FileProcessor:
    IMAGE_TYPES = {
        ContentType.IMAGE_JPEG, ContentType.IMAGE_PNG,
        ContentType.IMAGE_GIF, ContentType.IMAGE_WEBP
    }
    
    DOCUMENT_FORMAT_MAP = {
        ".pdf": "pdf", ".docx": "docx", ".csv": "csv",
        ".txt": "txt", ".html": "html", ".md": "md"
    }
    
    @staticmethod
    def validate_file_size(content: bytes, is_image: bool) -> None:
        max_size = MAX_IMAGE_SIZE if is_image else MAX_DOCUMENT_SIZE
        if len(content) > max_size:
            raise HTTPException(400, f"File too large: {len(content)} bytes. Max: {max_size} bytes")
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        name_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
        sanitized = re.sub(r'[^a-zA-Z0-9\s\-\(\)\[\]]', '', name_without_ext)
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        return sanitized or "document"
    
    @staticmethod
    def get_document_format(filename: str, content_type: str) -> str:
        for ext, fmt in FileProcessor.DOCUMENT_FORMAT_MAP.items():
            if filename.lower().endswith(ext):
                return fmt
        if "pdf" in content_type: return "pdf"
        elif "word" in content_type: return "docx"
        elif "csv" in content_type: return "csv"
        elif "html" in content_type: return "html"
        return "txt"
    
    @classmethod
    def create_content_block(cls, file: UploadFile, content: bytes) -> Dict[str, Any]:
        content_type = file.content_type or ""
        filename = file.filename or "unknown"
        
        if any(img_type.value in content_type for img_type in cls.IMAGE_TYPES):
            cls.validate_file_size(content, is_image=True)
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": content_type,
                    "data": base64.b64encode(content).decode("utf-8")
                }
            }
        elif any(ext in filename.lower() for ext in cls.DOCUMENT_FORMAT_MAP.keys()) or \
             "pdf" in content_type or "word" in content_type or "csv" in content_type:
            cls.validate_file_size(content, is_image=False)
            doc_format = cls.get_document_format(filename, content_type)
            return {
                "type": "document",
                "document": {
                    "format": doc_format,
                    "name": cls.sanitize_filename(filename),
                    "source": {"bytes": content}
                }
            }
        else:
            try:
                text_content = content.decode('utf-8')
                return {"type": "text", "text": f"[File: {filename}]\n{text_content[:1000]}"}
            except UnicodeDecodeError:
                raise HTTPException(400, f"Unsupported file type: {content_type}")

async def process_files(files: Optional[List[UploadFile]]) -> List[Dict[str, Any]]:
    if not files:
        return []
    
    content_blocks = []
    image_count = document_count = 0
    
    for file in files:
        content = await file.read()
        content_block = FileProcessor.create_content_block(file, content)
        
        if content_block["type"] == "image":
            image_count += 1
            if image_count > MAX_IMAGES:
                raise HTTPException(400, f"Too many images. Max: {MAX_IMAGES}")
        elif content_block["type"] == "document":
            document_count += 1
            if document_count > MAX_DOCUMENTS:
                raise HTTPException(400, f"Too many documents. Max: {MAX_DOCUMENTS}")
        
        content_blocks.append(content_block)
    
    return content_blocks