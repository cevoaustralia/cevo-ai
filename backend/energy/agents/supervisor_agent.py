from typing import TYPE_CHECKING
from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

if TYPE_CHECKING:
    from ..energy_chatbot import AgentState

llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-east-1",
)

@tool
def route_to_bill_explorer() -> str:
    """Route to bill explorer agent for existing customers who need help with their energy bills, usage analysis, or billing questions."""
    return "bill_explorer"

@tool
def route_to_switch_agent() -> str:
    """Route to switch agent for customers wanting to compare energy plans or switch providers."""
    return "switch_agent"

@tool
def route_to_brand_new_agent() -> str:
    """Route to brand new agent for customers who need new energy service connections or are new to the energy company."""
    return "brand_new_agent"

def supervisor_agent(state: "AgentState") -> "AgentState":
    messages = state["messages"]
    user_message = messages[-1] if messages else "Customer inquiry"
    
    tools = [route_to_bill_explorer, route_to_switch_agent, route_to_brand_new_agent]
    llm_with_tools = llm.bind_tools(tools)
    
    prompt = f"""You are a supervisor agent for an energy company. Based on the customer's message, decide which specialist agent should handle their request.
    
Customer message: {user_message}
    
Choose the appropriate routing tool."""
    
    try:
        response = llm_with_tools.invoke([HumanMessage(content=prompt)])
        if response.tool_calls:
            next_agent = response.tool_calls[0]["name"].replace("route_to_", "")
            messages.append(f"Supervisor: Routing to {next_agent.replace('_', ' ').title()} based on request analysis")
        else:
            next_agent = "bill_explorer"
            messages.append("Supervisor: Defaulting to Bill Explorer")
    except Exception:
        next_agent = "bill_explorer"
        messages.append("Supervisor: Defaulting to Bill Explorer")
    
    return {**state, "messages": messages, "next_agent": next_agent, "required_user_input": False, "input_needed": None}