import json
from typing import Dict, Optional

class MockEnergyAgentSystem:
    def __init__(self):
        pass
    
    def supervisor_agent(self, query: str) -> Dict:
        """Mock supervisor agent routing"""
        if any(word in query.lower() for word in ['bill', 'account', 'payment', 'usage']):
            return {"agent": "CURRENT_CUSTOMER", "reasoning": "Query about billing/account"}
        return {"agent": "NEW_CUSTOMER", "reasoning": "New customer inquiry"}
    
    def current_customer_agent(self, query: str, customer_number: Optional[str] = None) -> str:
        """Mock current customer agent"""
        if not customer_number:
            return "Please provide your customer number to access your account information."
        
        if customer_number == "12345":
            return f"Based on your account {customer_number}, your bill is high due to increased usage during winter months."
        return "Customer account information retrieved successfully."
    
    def new_customer_agent(self, query: str, address: Optional[str] = None) -> str:
        """Mock new customer agent"""
        if address and any(city in address.lower() for city in ['melbourne', 'sydney', 'brisbane']):
            return f"Great! We can provide energy services at {address}. Let me help you get started."
        return "Please provide your address so we can check service availability."
    
    def process_query(self, query: str, conversation_history: Optional[list] = None) -> Dict:
        """Mock main query processing"""
        # Extract info from conversation if available
        customer_number = None
        address = None
        
        if conversation_history:
            import re
            for msg in conversation_history:
                if msg.get('type') == 'user':
                    content = msg.get('content', '')
                    if not customer_number:
                        match = re.search(r'\b\d{4,6}\b', content)
                        if match:
                            customer_number = match.group()
                    if any(word in content.lower() for word in ['street', 'st', 'road', 'rd']):
                        address = content
        
        routing = self.supervisor_agent(query)
        
        if routing["agent"] == "CURRENT_CUSTOMER":
            response = self.current_customer_agent(query, customer_number)
        else:
            response = self.new_customer_agent(query, address)
        
        return {
            "response": response,
            "agent_used": routing["agent"],
            "reasoning": routing["reasoning"]
        }