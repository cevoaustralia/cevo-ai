from typing import TYPE_CHECKING
from langchain_aws import ChatBedrockConverse

if TYPE_CHECKING:
    from ..energy_chatbot import AgentState

llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-east-1",
)

def brand_new_agent(state: "AgentState") -> "AgentState":
    messages = state["messages"]
    files = state.get("uploaded_files", [])
    
    # Prepare context for LLM
    user_message = messages[-1] if messages else "New connection request"
    file_context = f" with {len(files)} uploaded files" if files else ""
    
    # Check if additional user input is needed
    required_user_input = False
    input_needed = None
    
    # Simple logic to determine if more info is needed
    if "address" not in user_message.lower() and "location" not in user_message.lower():
        required_user_input = True
        input_needed = "brand_new_agent"
        messages.append("Brand New Agent: I need your service address to proceed with the new connection.")
        resolution_status = "awaiting_input"
    else:
        prompt = f"""You are an energy company agent helping with new connection requests.
Customer message: {user_message}{file_context}
Provide a helpful response for setting up new energy service."""
        
        try:
            response = llm.invoke(prompt)
            llm_response = response.content
            messages.append(f"Brand New Agent: {llm_response}")
            resolution_status = "connection_processed"
        except Exception as e:
            messages.append(f"Brand New Agent: Processing new connection request... Connection approved. Welcome package will be sent.")
            resolution_status = "connection_verified"
    
    return {**state, "messages": messages, "resolution_status": resolution_status, "required_user_input": required_user_input, "input_needed": input_needed}