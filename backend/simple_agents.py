from typing import Dict, Optional

class SimpleEnergyAgentSystem:
    def process_query(self, query: str, conversation_history: Optional[list] = None) -> Dict:
        """Simple agent system without external dependencies"""
        try:
            query_lower = query.lower()
            
            # Simple greeting
            if any(word in query_lower for word in ['hi', 'hello', 'hey']):
                return {
                    "response": "Hello! I'm your Energy Assistant. I can help with account questions, bills, and new connections. How can I assist you today?",
                    "agent_used": "GREETING",
                    "reasoning": "Greeting detected"
                }
            
            # Current customer queries
            if any(word in query_lower for word in ['bill', 'account', 'payment', 'usage']):
                return {
                    "response": "I can help with your energy bill and account. Please provide your customer number so I can access your account information.",
                    "agent_used": "CURRENT_CUSTOMER", 
                    "reasoning": "Billing inquiry detected"
                }
            
            # New customer queries
            return {
                "response": "I can help you with energy services, switching providers, or new connections. What would you like to know?",
                "agent_used": "NEW_CUSTOMER",
                "reasoning": "General inquiry"
            }
            
        except Exception as e:
            print(f"Simple agent error: {e}")
            return {
                "response": "Hello! I'm your Energy Assistant. How can I help you today?",
                "agent_used": "FALLBACK",
                "reasoning": "System fallback"
            }