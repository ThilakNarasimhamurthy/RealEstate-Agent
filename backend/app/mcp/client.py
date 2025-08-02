# app/mcp/client.py
"""
MCP (Model Context Protocol) client manager for handling tool/server connections.
"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class MCPClientManager:
    """Manages connections to MCP servers and tools."""
    
    def __init__(self):
        self.connections: Dict[str, Any] = {}
        
    def register_server(self, name: str, server_instance: Any) -> None:
        """Register an MCP server instance."""
        self.connections[name] = server_instance
        logger.info(f"Registered MCP server: {name}")
        
    def get_server(self, name: str) -> Optional[Any]:
        """Get a registered server by name."""
        return self.connections.get(name)
        
    def list_servers(self) -> list[str]:
        """List all registered server names."""
        return list(self.connections.keys())
        
    def close_all(self) -> None:
        """Close all server connections."""
        for name in list(self.connections.keys()):
            if hasattr(self.connections[name], 'close'):
                self.connections[name].close()
            del self.connections[name]
        logger.info("Closed all MCP server connections") 