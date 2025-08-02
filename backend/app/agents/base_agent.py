# app/agents/base_agent.py
"""
Base agent class - foundation for all agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.{name}")
        
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """Process input data and return output."""
        pass
        
    @abstractmethod
    def can_handle(self, input_data: Any) -> bool:
        """Check if this agent can handle the given input."""
        pass
        
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information."""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "config": self.config,
            "active": True
        }
        
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Update agent configuration."""
        self.config.update(new_config)
        self.logger.info(f"Updated configuration for agent {self.name}")
        
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities."""
        return []
        
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data. Override in subclasses if needed."""
        return True
        
    def preprocess(self, input_data: Any) -> Any:
        """Preprocess input data. Override in subclasses if needed."""
        return input_data
        
    def postprocess(self, output_data: Any) -> Any:
        """Postprocess output data. Override in subclasses if needed."""
        return output_data 