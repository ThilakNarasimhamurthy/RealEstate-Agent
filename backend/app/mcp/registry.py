# app/mcp/registry.py
"""
MCP (Model Context Protocol) tool and server registry.
"""

from typing import Dict, Any, Callable, Optional
import logging

logger = logging.getLogger(__name__)

class MCPRegistry:
    """Registry for MCP tools and servers."""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.servers: Dict[str, Any] = {}
        
    def register_tool(self, name: str, tool_func: Callable) -> None:
        """Register a tool function."""
        self.tools[name] = tool_func
        logger.info(f"Registered MCP tool: {name}")
        
    def register_server(self, name: str, server_instance: Any) -> None:
        """Register a server instance."""
        self.servers[name] = server_instance
        logger.info(f"Registered MCP server: {name}")
        
    def get_tool(self, name: str) -> Optional[Callable]:
        """Get a registered tool by name."""
        return self.tools.get(name)
        
    def get_server(self, name: str) -> Optional[Any]:
        """Get a registered server by name."""
        return self.servers.get(name)
        
    def list_tools(self) -> list[str]:
        """List all registered tool names."""
        return list(self.tools.keys())
        
    def list_servers(self) -> list[str]:
        """List all registered server names."""
        return list(self.servers.keys())
        
    def unregister_tool(self, name: str) -> bool:
        """Unregister a tool. Returns True if tool was found and removed."""
        if name in self.tools:
            del self.tools[name]
            logger.info(f"Unregistered MCP tool: {name}")
            return True
        return False
        
    def unregister_server(self, name: str) -> bool:
        """Unregister a server. Returns True if server was found and removed."""
        if name in self.servers:
            del self.servers[name]
            logger.info(f"Unregistered MCP server: {name}")
            return True
        return False 