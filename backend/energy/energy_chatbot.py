from typing import Annotated, Dict, List, Optional, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
import operator
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import uvicorn
from langgraph.checkpoint.memory import MemorySaver
from agents import supervisor_agent, switch_agent, brand_new_agent
from utils.file_processor import process_files

class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    customer_id: Optional[str]
    customer_type: str  # "existing", "external", "new"
    issue_type: Optional[str]
    bill_data: Optional[Dict]
    energy_plan: Optional[str]
    next_agent: Optional[str]
    resolution_status: str
    uploaded_files: Optional[List[Any]]
    required_user_input: bool
    input_needed: Optional[str]

def bill_explorer_agent(state: AgentState) -> AgentState:
    messages = state["messages"]
    files = state.get("uploaded_files", [])
    messages.append("Bill Explorer: Accessing customer bill data...")
    
    if files:
        messages.append(f"Bill Explorer: Processing {len(files)} uploaded file(s) for bill analysis...")
        bill_data = {"parsed_from_file": True, "files_processed": len(files)}
    else:
        bill_data = {
            "account_id": state.get("customer_id"),
            "current_charges": 245.67,
            "usage_kwh": 892,
            "plan_type": "Standard Residential",
            "billing_period": "Sept 15 - Oct 15",
            "previous_balance": 0.00,
            "payment_due": "Nov 1, 2025"
        }
    messages.append("Bill Explorer: Bill analysis complete.")
    return {**state, "messages": messages, "bill_data": bill_data, "resolution_status": "bill_explained", "required_user_input": False, "input_needed": None}

def route_to_agent(state: AgentState) -> str:
    return state.get("next_agent", END)

def create_customer_service_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("bill_explorer", bill_explorer_agent)
    workflow.add_node("switch_agent", switch_agent)
    workflow.add_node("brand_new_agent", brand_new_agent)
    workflow.set_entry_point("supervisor")
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "bill_explorer": "bill_explorer",
            "switch_agent": "switch_agent", 
            "brand_new_agent": "brand_new_agent"
        }
    )
    workflow.add_edge("bill_explorer", END)
    workflow.add_edge("switch_agent", END)
    workflow.add_edge("brand_new_agent", END)
    return workflow.compile(checkpointer=checkpointer)

class ChatRequest(BaseModel):
    message: str
    customer_id: Optional[str] = None
    customer_type: str = "existing"
    start_at: Optional[str] = None

app = FastAPI(title="Energy Chatbot API")
checkpointer = MemorySaver()
graph = create_customer_service_graph()

@app.post("/threads/{thread_id}/chat")
async def chat_endpoint(
    thread_id: str,
    message: str = Form(...),
    customer_id: Optional[str] = Form(None),
    customer_type: str = Form("existing"),
    files: List[UploadFile] = File(None),
    start_at: Optional[str] = Form(None)
):
    # Process files using FileProcessor
    processed_files = await process_files(files)
    
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        state = checkpointer.get(config)
        if state:
            current_state = state.values
            current_state["messages"].append(f"User: {message}")
            current_state["uploaded_files"] = processed_files
        else:
            current_state = {
                "messages": [f"User: {message}"],
                "customer_id": customer_id,
                "customer_type": customer_type,
                "issue_type": None,
                "bill_data": None,
                "energy_plan": None,
                "next_agent": None,
                "resolution_status": "pending",
                "uploaded_files": processed_files,
                "required_user_input": False,
                "input_needed": None
            }
    except:
        current_state = {
            "messages": [f"User: {message}"],
            "customer_id": customer_id,
            "customer_type": customer_type,
            "issue_type": None,
            "bill_data": None,
            "energy_plan": None,
            "next_agent": None,
            "resolution_status": "pending",
            "uploaded_files": processed_files,
            "required_user_input": False,
            "input_needed": None
        }
    
    # Direct invocation to specific agent if start_at is provided
    if start_at:
        result = graph.invoke(current_state, config, start_at=start_at)
    else:
        result = graph.invoke(current_state, config)
    
    return {
        "messages": result["messages"],
        "resolution_status": result["resolution_status"],
        "bill_data": result.get("bill_data"),
        "energy_plan": result.get("energy_plan"),
        "files_processed": len(processed_files),
        "required_user_input": result.get("required_user_input", False),
        "input_needed": result.get("input_needed")
    }

@app.get("/threads/{thread_id}/messages")
async def get_messages(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    try:
        state = checkpointer.get(config)
        if state and "messages" in state.values:
            return {"messages": state.values["messages"]}
        return {"messages": []}
    except:
        return {"messages": []}

@app.delete("/threads/{thread_id}")
async def delete_thread(thread_id: str):
    return {"status": "success", "message": f"Thread {thread_id} cleared"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
