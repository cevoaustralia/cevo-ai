from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from mock_agents import MockEnergyAgentSystem

class ChatRequest(BaseModel):
    query: str
    customer_number: Optional[str] = None
    address: Optional[str] = None

app = FastAPI()
agent_system = MockEnergyAgentSystem()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        result = agent_system.process_query(
            query=request.query,
            customer_number=request.customer_number,
            address=request.address
        )
        return result
    except Exception as e:
        return {
            "response": f"Error processing request: {str(e)}",
            "agent_used": "ERROR",
            "reasoning": "System error occurred"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2024)