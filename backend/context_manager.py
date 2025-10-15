import uuid
from typing import Dict, Optional, Any
from datetime import datetime, timedelta

class ConversationContext:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.customer_number: Optional[str] = None
        self.address: Optional[str] = None
        self.customer_data: Optional[Dict] = None
        self.current_agent: Optional[str] = None
        self.conversation_history: list = []
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
    
    def update_customer_number(self, customer_number: str):
        self.customer_number = customer_number
        self.last_updated = datetime.now()
    
    def update_address(self, address: str):
        self.address = address
        self.last_updated = datetime.now()
    
    def update_customer_data(self, data: Dict):
        self.customer_data = data
        self.last_updated = datetime.now()
    
    def set_current_agent(self, agent: str):
        self.current_agent = agent
        self.last_updated = datetime.now()
    
    def add_message(self, message_type: str, content: str, agent: str = None):
        self.conversation_history.append({
            'type': message_type,
            'content': content,
            'agent': agent,
            'timestamp': datetime.now().isoformat()
        })
        self.last_updated = datetime.now()

class ContextManager:
    def __init__(self):
        self.contexts: Dict[str, ConversationContext] = {}
        self.session_timeout = timedelta(hours=2)
    
    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.contexts[session_id] = ConversationContext(session_id)
        return session_id
    
    def get_context(self, session_id: str) -> Optional[ConversationContext]:
        if session_id in self.contexts:
            context = self.contexts[session_id]
            # Check if session expired
            if datetime.now() - context.last_updated > self.session_timeout:
                del self.contexts[session_id]
                return None
            return context
        return None
    
    def cleanup_expired_sessions(self):
        expired_sessions = []
        for session_id, context in self.contexts.items():
            if datetime.now() - context.last_updated > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.contexts[session_id]

# Global context manager instance
context_manager = ContextManager()