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

from utils.file_processor import process_files


# Initialize LLM with ChatBedrockConverse
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-east-1",
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
                                "content_type": "markdown",
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
