import json
import re
import os
from typing import Dict, List, Optional
from database import EnergyDatabase

try:
    from langchain_aws import ChatBedrock
    from langchain_core.messages import HumanMessage, SystemMessage
    BEDROCK_AVAILABLE = True
except ImportError:
    BEDROCK_AVAILABLE = False

class EnergyAgentSystem:
    def __init__(self):
        aws_token = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
        print(f"AWS Token available: {bool(aws_token)}")
        print(f"Bedrock available: {BEDROCK_AVAILABLE}")
        
        # Disable Bedrock for now due to permissions issue
        self.use_bedrock = False
        print("Using fallback mode (Bedrock disabled)")
        self.db = EnergyDatabase()
        
    def check_address_availability(self, address: str) -> str:
        """Check if energy services are available at the given address"""
        try:
            is_available = self.db.check_address_coverage(address)
            if is_available:
                return f"Energy services are available at {address}"
            return f"Energy services may not be available at {address}. Please contact support."
        except Exception as e:
            # Fallback check
            if any(suburb in address.lower() for suburb in ['sydney', 'melbourne', 'brisbane', 'perth', 'adelaide']):
                return f"Energy services are available at {address}"
            return f"Energy services may not be available at {address}. Please contact support."
    
    def get_customer_data(self, customer_number: str) -> str:
        """Retrieve customer data from energy database"""
        try:
            customer_data = self.db.get_customer_by_number(customer_number)
            if customer_data:
                return json.dumps(customer_data)
            return "Customer not found"
        except Exception as e:
            # Fallback to mock data if database unavailable
            mock_data = {
                "12345": {
                    "name": "John Smith",
                    "address": "123 Main St, Sydney NSW 2000",
                    "current_bill": 450.50,
                    "usage_kwh": 850,
                    "rate": 0.28,
                    "account_status": "active"
                }
            }
            if customer_number in mock_data:
                return json.dumps(mock_data[customer_number])
            return "Customer not found"
    
    def supervisor_agent(self, query: str) -> Dict:
        """Analyzes query and routes to appropriate agent"""
        try:
            if self.use_bedrock:
                try:
                    system_prompt = """You are a Supervisor Agent for an energy retailer. 
                    Analyze the customer query and determine if they are:
                    1. CURRENT_CUSTOMER - existing customer with billing/account questions
                    2. NEW_CUSTOMER - wants to switch providers or new connection
                    
                    Respond with JSON: {"agent": "CURRENT_CUSTOMER" or "NEW_CUSTOMER", "reasoning": "brief explanation"}"""
                    
                    messages = [
                        SystemMessage(content=system_prompt),
                        HumanMessage(content=query)
                    ]
                    
                    response = self.llm.invoke(messages)
                    return json.loads(response.content)
                except Exception as e:
                    print(f"Bedrock error: {e}")
            
            # Fallback routing logic
            if any(word in query.lower() for word in ['bill', 'account', 'payment', 'usage', 'customer number']):
                return {"agent": "CURRENT_CUSTOMER", "reasoning": "Query about billing/account"}
            return {"agent": "NEW_CUSTOMER", "reasoning": "New customer inquiry"}
        except Exception as e:
            print(f"Supervisor agent error: {e}")
            return {"agent": "NEW_CUSTOMER", "reasoning": "Default routing due to error"}
    
    def current_customer_agent(self, query: str, customer_number: Optional[str] = None) -> str:
        """Handles existing customer queries"""
        if not customer_number:
            return "Hello! I can help with your energy account. Please provide your customer number so I can access your account information."
        
        customer_data = self.get_customer_data(customer_number)
        
        if self.use_bedrock:
            try:
                system_prompt = f"""You are a Current Customer Agent for an energy retailer.
                Customer data: {customer_data}
                
                Help the customer with their billing and account questions. Be helpful and specific."""
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=query)
                ]
                
                response = self.llm.invoke(messages)
                return response.content
            except Exception as e:
                print(f"Bedrock error: {e}")
        
        # Fallback response
        if customer_data and customer_data != "Customer not found":
            data = json.loads(customer_data)
            return f"Hi! I can see your account for customer {customer_number}. Your current bill is ${data.get('current_bill', 0)}. How can I help you today?"
        return f"I found your customer number {customer_number}. How can I help with your energy account today?"
    
    def new_customer_agent(self, query: str, address: Optional[str] = None) -> str:
        """Handles new customer inquiries"""
        if self.use_bedrock:
            try:
                address_info = ""
                if address:
                    address_info = self.check_address_availability(address)
                
                system_prompt = f"""You are a New Customer Agent for an energy retailer.
                Help customers switch providers or set up new connections.
                
                Address availability: {address_info if address_info else "No address provided yet"}
                
                If no address provided, ask for it to check service availability."""
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=query)
                ]
                
                response = self.llm.invoke(messages)
                return response.content
            except Exception as e:
                print(f"Bedrock error: {e}")
        
        # Fallback response
        if address:
            availability = self.check_address_availability(address)
            return f"Hi! I can help you with energy services. {availability} What would you like to know about switching or setting up a new connection?"
        return "Hello! I can help you switch energy providers or set up a new connection. Could you please provide your address so I can check service availability?"
    
    def extract_customer_info(self, query: str, conversation_history: list) -> Dict:
        """Extract customer number and address from conversation"""
        # Look for customer number in current query and history
        import re
        customer_number = None
        address = None
        
        # Check current query
        customer_match = re.search(r'\b\d{4,6}\b', query)
        if customer_match:
            customer_number = customer_match.group()
        
        # Check conversation history
        for msg in conversation_history:
            if msg.get('type') == 'user':
                content = msg.get('content', '')
                if not customer_number:
                    customer_match = re.search(r'\b\d{4,6}\b', content)
                    if customer_match:
                        customer_number = customer_match.group()
                
                # Look for address patterns
                if any(word in content.lower() for word in ['street', 'st', 'road', 'rd', 'avenue', 'ave']):
                    address = content
        
        return {'customer_number': customer_number, 'address': address}
    
    def process_query(self, query: str, conversation_history: Optional[list] = None) -> Dict:
        """Main entry point for processing customer queries"""
        try:
            if conversation_history is None:
                conversation_history = []
                
            # Extract customer info from conversation
            customer_info = self.extract_customer_info(query, conversation_history)
            
            # Route through supervisor
            routing = self.supervisor_agent(query)
            
            if routing["agent"] == "CURRENT_CUSTOMER":
                response = self.current_customer_agent(query, customer_info['customer_number'])
            else:
                response = self.new_customer_agent(query, customer_info['address'])
            
            return {
                "response": response,
                "agent_used": routing["agent"],
                "reasoning": routing["reasoning"]
            }
        except Exception as e:
            print(f"Process query error: {e}")
            return {
                "response": "Hello! I'm your Energy Assistant. How can I help you today?",
                "agent_used": "FALLBACK",
                "reasoning": "System fallback due to error"
            }