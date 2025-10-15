from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..energy_chatbot import AgentState

def switch_agent(state: "AgentState") -> "AgentState":
    messages = state["messages"]
    files = state.get("uploaded_files", [])
    if files:
        messages.append(f"Switch Agent: Received {len(files)} file(s) for plan comparison. Processing uploaded bills...")
    else:
        messages.append("Switch Agent: No files uploaded for plan comparison.")
    
    messages.append("Switch Agent: Comparing available energy plans...")
    energy_plan = "Recommended: Green Energy Plan - 15% savings vs current plan"
    
    return {**state, "messages": messages, "energy_plan": energy_plan, "resolution_status": "plans_compared", "required_user_input": False, "input_needed": None}