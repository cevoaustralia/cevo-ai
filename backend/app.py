from langchain_aws import ChatBedrock
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os


# Initialize LLM with Bedrock API key from environment
# Set AWS_BEARER_TOKEN_BEDROCK environment variable before running
llm = ChatBedrock(
    model_id="anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
)


# Create agent
agent = create_react_agent(llm, tools=[])


app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/invoke")
async def invoke_agent(request: dict):
    messages = request.get("messages", [])
    result = agent.invoke({"messages": messages})
    return {"messages": result["messages"]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2024)
