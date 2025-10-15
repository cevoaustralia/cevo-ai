from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import re
from typing import Optional
from context_manager import context_manager, ConversationContext

try:
    from langchain_aws import ChatBedrock
    from langchain_core.messages import HumanMessage, SystemMessage
    BEDROCK_AVAILABLE = True
except ImportError:
    BEDROCK_AVAILABLE = False

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    conversation_history: Optional[list] = None
    has_file: Optional[bool] = False
    file_name: Optional[str] = None

app = FastAPI()

# Initialize Bedrock if available
llm = None
if BEDROCK_AVAILABLE and os.getenv('AWS_BEARER_TOKEN_BEDROCK'):
    try:
        llm = ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="ap-southeast-2",
        )
        print("Bedrock initialized successfully")
    except Exception as e:
        print(f"Bedrock initialization failed: {e}")
        llm = None
else:
    print("Using fallback mode (no Bedrock)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy"}

def extract_info_from_query(query: str, context: ConversationContext):
    """Extract customer number and address from query and update context"""
    # Extract customer number
    customer_match = re.search(r'\b\d{4,6}\b', query)
    if customer_match and not context.customer_number:
        context.update_customer_number(customer_match.group())
    
    # Extract address
    if any(word in query.lower() for word in ['street', 'st', 'road', 'rd', 'avenue', 'ave']) and not context.address:
        context.update_address(query)

def supervisor_agent(query: str, context: ConversationContext) -> dict:
    """Routes query to appropriate agent with context awareness"""
    # Extract info from current query
    extract_info_from_query(query, context)
    
    # Use existing agent if context suggests continuity
    if context.current_agent and context.customer_number:
        return {"agent": context.current_agent, "reasoning": "Continuing with established context"}
    
    if llm:
        try:
            context_info = f"Customer number: {context.customer_number or 'None'}, Address: {context.address or 'None'}"
            system_prompt = f"""You are a Supervisor Agent for an energy retailer. 
            Context: {context_info}
            
            Analyze the customer query and determine if they are:
            1. CURRENT_CUSTOMER - existing customer with billing/account questions
            2. NEW_CUSTOMER - wants to switch providers or new connection
            
            Respond with only: CURRENT_CUSTOMER or NEW_CUSTOMER"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=query)
            ]
            response = llm.invoke(messages)
            agent_type = response.content.strip()
            
            if "CURRENT_CUSTOMER" in agent_type:
                return {"agent": "CURRENT_CUSTOMER", "reasoning": "Billing/account query"}
            else:
                return {"agent": "NEW_CUSTOMER", "reasoning": "New customer inquiry"}
        except:
            pass
    
    # Fallback routing with context awareness
    if context.customer_number or any(word in query.lower() for word in ['bill', 'account', 'payment', 'usage']):
        return {"agent": "CURRENT_CUSTOMER", "reasoning": "Billing/account query"}
    return {"agent": "NEW_CUSTOMER", "reasoning": "New customer inquiry"}

def current_customer_agent(query: str, context: ConversationContext) -> str:
    """Handles current customer queries with shared context"""
    if not context.customer_number:
        return "I can help with your energy account. Please provide your customer number so I can access your account information."
    
    # Mock customer data lookup
    if not context.customer_data:
        mock_data = {
            "name": "Customer",
            "current_bill": 450.50,
            "usage_kwh": 850,
            "account_status": "active"
        }
        context.update_customer_data(mock_data)
    
    if llm:
        try:
            system_prompt = f"""You are a Current Customer Agent for an energy retailer.
            Customer #{context.customer_number}: {context.customer_data}
            
            Help with billing, account questions, and usage inquiries using the customer data."""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=query)
            ]
            response = llm.invoke(messages)
            return response.content
        except:
            pass
    
    return f"Hi! I can see your account #{context.customer_number}. Your current bill is ${context.customer_data['current_bill']}. How can I help you today?"

def new_customer_agent(query: str, context: ConversationContext) -> str:
    """Handles new customer queries with shared context"""
    if llm:
        try:
            address_info = f"Address: {context.address}" if context.address else "No address provided yet"
            system_prompt = f"""You are a New Customer Agent for an energy retailer.
            Context: {address_info}
            
            Help customers switch providers or set up new connections.
            If no address, ask for it to check service availability."""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=query)
            ]
            response = llm.invoke(messages)
            return response.content
        except:
            pass
    
    if context.address:
        return f"Hi! I can help you with energy services at {context.address}. What would you like to know about switching or setting up a new connection?"
    return "I can help you switch energy providers or set up a new connection. Could you provide your address so I can check service availability?"

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Get or create session context
        if not request.session_id:
            session_id = context_manager.create_session()
        else:
            session_id = request.session_id
        
        context = context_manager.get_context(session_id)
        if not context:
            session_id = context_manager.create_session()
            context = context_manager.get_context(session_id)
        
        # Add user message to context
        context.add_message('user', request.query)
        
        # Route through supervisor with context
        routing = supervisor_agent(request.query, context)
        context.set_current_agent(routing["agent"])
        
        # Process with appropriate agent
        if routing["agent"] == "CURRENT_CUSTOMER":
            response = current_customer_agent(request.query, context)
        else:
            response = new_customer_agent(request.query, context)
        
        # Add assistant response to context
        context.add_message('assistant', response, routing["agent"])
        
        return {
            "response": response,
            "agent_used": routing["agent"],
            "reasoning": routing["reasoning"],
            "session_id": session_id,
            "context": {
                "customer_number": context.customer_number,
                "address": context.address,
                "current_agent": context.current_agent
            }
        }
        
    except Exception as e:
        print(f"Chat error: {e}")
        return {
            "response": "Hello! I'm your Energy Assistant. How can I help you today?",
            "agent_used": "FALLBACK",
            "reasoning": "System fallback",
            "session_id": context_manager.create_session()
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2024)
