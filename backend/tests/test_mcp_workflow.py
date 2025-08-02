#!/usr/bin/env python3
"""
Test MCP workflow: servers, tools, and agent-orchestrator integration.
"""

from app.mcp.servers import RAGServer, CRMServer
from app.mcp.tools import DatabaseTools, LLMTools
from app.agents import OrchestratorAgent
from app.agents.data import RAGAgent, CRMAgent
from app.agents.conversational import ChatAgent

print("\n=== MCP SERVER TESTS ===")

# Test RAGServer
rag_server = RAGServer()
print("RAGServer stats:", rag_server.get_stats())

# (Optional) Test document ingestion and search (uncomment if you have a file)
# rag_server.ingest_document("data/uploads/sample.txt")
# print("RAGServer search:", rag_server.search_documents("test query"))

# Test DatabaseTools
db_tools = DatabaseTools()
print("Database tables:", db_tools.list_tables())

# Test LLMTools
llm_tools = LLMTools()
print("LLM model info:", llm_tools.get_model_info())

print("\n=== MCP AGENT + ORCHESTRATOR TESTS ===")

# Create agents
rag_agent = RAGAgent()
rag_agent.set_vector_db(rag_server)
crm_agent = CRMAgent()
# CRMServer requires a db_session, so we skip full integration here
chat_agent = ChatAgent()

# Create orchestrator and register agents
orchestrator = OrchestratorAgent()
orchestrator.register_agent(rag_agent)
orchestrator.register_agent(crm_agent)
orchestrator.register_agent(chat_agent)

# Test orchestrator routing to chat agent
input_data = "Hello, how can I use the RAG system?"
output = orchestrator.process(input_data)
print("Orchestrator chat output:", output)

# Test orchestrator routing to RAG agent (search)
rag_input = {"operation": "search", "query": "AI"}
output = orchestrator.process(rag_input)
print("Orchestrator RAG search output:", output)

print("\n=== MCP WORKFLOW TEST COMPLETE ===") 