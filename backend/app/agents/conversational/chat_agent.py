# app/agents/conversational/chat_agent.py
"""
Chat agent - main conversation logic.
"""

from typing import Dict, Any, List, Optional
from ..base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class ChatAgent(BaseAgent):
    """Handles conversational interactions and chat logic."""
    
    def __init__(self, name: str = "chat_agent", config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history_length = config.get("max_history_length", 50) if config else 50
        
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        message = {"role": role, "content": content}
        self.conversation_history.append(message)
        
        # Keep history within limits
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
            
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()
        
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
        self.logger.info("Cleared conversation history")
        
    def process(self, input_data: Any) -> Any:
        """Process chat input and return response."""
        if isinstance(input_data, dict):
            role = input_data.get("role", "user")
            content = input_data.get("content", "")
        elif isinstance(input_data, str):
            role = "user"
            content = input_data
        else:
            raise ValueError("Input must be a string or dict with 'content' key")
            
        # Add user message to history
        self.add_message(role, content)
        
        # Generate response (this would typically use an LLM)
        response = self._generate_response(content)
        
        # Add assistant response to history
        self.add_message("assistant", response)
        
        return {
            "response": response,
            "history": self.get_conversation_history()
        }
        
    def _generate_response(self, user_message: str) -> str:
        """Generate a response to the user message."""
        # This is a placeholder - in a real implementation, this would use an LLM
        # For now, return a simple echo response
        return f"I received your message: '{user_message}'. This is a placeholder response."
        
    def can_handle(self, input_data: Any) -> bool:
        """Check if this agent can handle the input."""
        if isinstance(input_data, str):
            return True
        elif isinstance(input_data, dict):
            return "content" in input_data
        return False
        
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return [
            "conversation",
            "chat",
            "message_history",
            "context_awareness"
        ]
        
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get conversation statistics."""
        user_messages = sum(1 for msg in self.conversation_history if msg["role"] == "user")
        assistant_messages = sum(1 for msg in self.conversation_history if msg["role"] == "assistant")
        
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "max_history_length": self.max_history_length
        } 