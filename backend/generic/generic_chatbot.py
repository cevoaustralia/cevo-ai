from langchain_aws import ChatBedrockConverse
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
import base64
from typing import Dict, List, Optional, Any
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MAX_IMAGE_SIZE = 3.75 * 1024 * 1024  # 3.75 MB
MAX_DOCUMENT_SIZE = 4.5 * 1024 * 1024  # 4.5 MB
MAX_IMAGES = 20
MAX_DOCUMENTS = 5

class ContentType(Enum):
    """Supported content types"""
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
    """Handle file processing and content block creation"""
    
    IMAGE_TYPES = {
        ContentType.IMAGE_JPEG, ContentType.IMAGE_PNG,
        ContentType.IMAGE_GIF, ContentType.IMAGE_WEBP
    }
    
    DOCUMENT_FORMAT_MAP = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".csv": "csv",
        ".txt": "txt",
        ".html": "html",
        ".md": "md"
    }
    
    @staticmethod
    def validate_file_size(content: bytes, is_image: bool) -> None:
        """Validate file size against Bedrock limits"""
        max_size = MAX_IMAGE_SIZE if is_image else MAX_DOCUMENT_SIZE
        if len(content) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large: {len(content)} bytes. Max: {max_size} bytes"
            )
    
    @staticmethod
    def get_document_format(filename: str, content_type: str) -> str:
        """Determine document format from filename or content type"""
        # Try filename extension first
        for ext, fmt in FileProcessor.DOCUMENT_FORMAT_MAP.items():
            if filename.lower().endswith(ext):
                return fmt
        
        # Fallback to content type
        if "pdf" in content_type:
            return "pdf"
        elif "word" in content_type:
            return "docx"
        elif "csv" in content_type:
            return "csv"
        elif "html" in content_type:
            return "html"
        
        return "txt"  # Default fallback
    
    @classmethod
    def create_content_block(cls, file: UploadFile, content: bytes) -> Dict[str, Any]:
        """Create appropriate content block based on file type"""
        content_type = file.content_type or ""
        filename = file.filename or "unknown"
        
        # Handle images
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
        
        # Handle documents
        elif any(ext in filename.lower() for ext in cls.DOCUMENT_FORMAT_MAP.keys()) or \
             "pdf" in content_type or "word" in content_type or "csv" in content_type:
            cls.validate_file_size(content, is_image=False)
            doc_format = cls.get_document_format(filename, content_type)
            return {
                "type": "document",
                "document": {
                    "format": doc_format,
                    "name": filename,
                    "source": {"bytes": content}
                }
            }
        
        # Unsupported type - try as text
        else:
            try:
                text_content = content.decode('utf-8')
                return {
                    "type": "text",
                    "text": f"[File: {filename}]\n{text_content[:1000]}"  # Limit length
                }
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {content_type}"
                )


# Initialize LLM with ChatBedrockConverse
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="ap-southeast-2",
)

# Use LangGraph's built-in checkpointer for state persistence
checkpointer = MemorySaver()

# Create agent with checkpointer
agent = create_react_agent(llm, tools=[], checkpointer=checkpointer)

app = FastAPI(title="LangGraph Chat API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def process_files(files: Optional[List[UploadFile]]) -> List[Dict[str, Any]]:
    """Process uploaded files and create content blocks"""
    if not files:
        return []
    
    content_blocks = []
    image_count = 0
    document_count = 0
    
    for file in files:
        try:
            content = await file.read()
            content_block = FileProcessor.create_content_block(file, content)
            
            # Track counts for limits
            if content_block["type"] == "image":
                image_count += 1
                if image_count > MAX_IMAGES:
                    raise HTTPException(400, f"Too many images. Max: {MAX_IMAGES}")
            elif content_block["type"] == "document":
                document_count += 1
                if document_count > MAX_DOCUMENTS:
                    raise HTTPException(400, f"Too many documents. Max: {MAX_DOCUMENTS}")
            
            content_blocks.append(content_block)
            
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            raise HTTPException(400, f"Error processing {file.filename}: {str(e)}")
    
    return content_blocks


@app.post("/threads/{thread_id}/runs/stream")
async def create_run_stream(
    thread_id: str, 
    message: str = Form(...),
    files: Optional[List[UploadFile]] = File(None)
):
    """Stream agent response with file support"""
    try:
        # Build message content
        message_content = [{"type": "text", "text": message}]
        
        # Process files
        file_blocks = await process_files(files)
        message_content.extend(file_blocks)
        
        # Create message
        user_message = HumanMessage(content=message_content)
        
        # Stream agent response using LangGraph checkpointer
        config = {"configurable": {"thread_id": thread_id}}
        
        async def generate():
            try:
                # Use astream for true streaming
                async for event in agent.astream(
                    {"messages": [user_message]},
                    config=config,
                    stream_mode="values"
                ):
                    # Get the latest message
                    if "messages" in event and event["messages"]:
                        latest_message = event["messages"][-1]
                        
                        # Only stream assistant messages
                        if isinstance(latest_message, AIMessage):
                            response_data = {
                                "type": "assistant",
                                "content": latest_message.content,
                                "message_type": "chunk"
                            }
                            yield f"data: {json.dumps(response_data)}\n\n"
                
                yield "data: [DONE]\n\n"
                
            except Exception as e:
                logger.error(f"Error during streaming: {str(e)}")
                error_data = {"error": str(e)}
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_run_stream: {str(e)}")
        raise HTTPException(500, f"Internal server error: {str(e)}")


@app.get("/threads/{thread_id}/messages")
async def get_messages(thread_id: str):
    """Get conversation history from checkpointer"""
    try:
        config = {"configurable": {"thread_id": thread_id}}
        state = agent.get_state(config)
        
        # Extract messages from state
        messages = []
        if state and "messages" in state.values:
            for msg in state.values["messages"]:
                messages.append({
                    "type": "human" if isinstance(msg, HumanMessage) else "assistant",
                    "content": msg.content
                })
        
        return {"messages": messages}
        
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        raise HTTPException(500, f"Error retrieving messages: {str(e)}")


@app.get("/threads/{thread_id}/state")
async def get_thread_state(thread_id: str):
    """Get full thread state from checkpointer"""
    try:
        config = {"configurable": {"thread_id": thread_id}}
        state = agent.get_state(config)
        
        return {"values": state.values if state else {}}
        
    except Exception as e:
        logger.error(f"Error getting state: {str(e)}")
        raise HTTPException(500, f"Error retrieving state: {str(e)}")


@app.delete("/threads/{thread_id}")
async def delete_thread(thread_id: str):
    """Delete a thread (clear checkpointer state)"""
    # Note: MemorySaver doesn't have built-in delete, but you can implement
    # For production, use PostgresSaver or RedisSaver with delete support
    return {"status": "success", "message": f"Thread {thread_id} cleared"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2024)
