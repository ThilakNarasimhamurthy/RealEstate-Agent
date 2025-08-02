# app/agents/orchestrator.py
"""
Orchestrator agent - coordinates all other agents and manages workflow.
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import logging
from app.services.mongo_conversation_service import MongoConversationService
from app.services.mongo_message_service import MongoMessageService
from bson import ObjectId

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseAgent):
    """Orchestrates multiple agents to handle complex tasks."""
    
    def __init__(self, name: str = "orchestrator", config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.agents: Dict[str, BaseAgent] = {}
        self.workflows: Dict[str, List[str]] = {}
        
        # Initialize specific agents for MCP compatibility
        self._init_agents()
        
    def _init_agents(self):
        """Initialize the specific agents needed for MCP"""
        try:
            from .data.rag_agent import RAGAgent
            from .data.crm_agent import CRMAgent
            from .conversational.chat_agent import ChatAgent
            
            self.rag_agent = RAGAgent()
            self.crm_agent = CRMAgent()
            self.chat_agent = ChatAgent() if hasattr(self, 'ChatAgent') else None
            
            # Register them
            self.register_agent(self.rag_agent)
            self.register_agent(self.crm_agent)
            if self.chat_agent:
                self.register_agent(self.chat_agent)
                
        except ImportError as e:
            logger.warning(f"Could not import all agents: {e}")
            # Create minimal agents for testing
            self.rag_agent = RAGAgent()
            self.crm_agent = CRMAgent()
            self.chat_agent = None
    
    # ADD MISSING METHOD: process_chat_request
    async def process_chat_request(self, message: str, user_id: str, conversation_id: Optional[str] = None) -> dict:
        """Process a chat request using MCP architecture with persistent conversation memory"""
        try:
            self.logger.info(f"Starting chat request processing for user: {user_id}")
            
            # --- STEP 1: Robust User ID Resolution ---
            mongo_user_id = None
            user = None
            # Try to interpret user_id as ObjectId
            try:
                mongo_user_id = str(ObjectId(user_id))
                # Fetch user by ObjectId
                self.logger.info(f"Trying to get user by ObjectId: {mongo_user_id}")
                user = await self.crm_agent.user_service.get_user_by_id(mongo_user_id)
                if not user:
                    # If not found, treat as email
                    raise Exception("User not found by ObjectId, fallback to email")
            except Exception as e:
                self.logger.info(f"ObjectId lookup failed: {e}, trying email approach")
                # Not a valid ObjectId or not found, treat as email
                # Extract user info from message if possible
                self.logger.info("Extracting user info from message")
                extracted_info = self.crm_agent.extract_user_info(message)
                self.logger.info(f"Extracted info: {extracted_info}")
                email = user_id if "@" in user_id else (extracted_info.get("email") if extracted_info else None)
                user_info = {"email": email}
                if extracted_info:
                    user_info.update(extracted_info)
                self.logger.info(f"User info for get_or_create_user: {user_info}")
                user = await self.crm_agent.get_or_create_user(user_info)
                mongo_user_id = str(user["_id"])
            if user is None:
                raise ValueError("User not found or could not be created.")
            # --- END STEP 1 ---
            # CRM actions: log user creation/update (placeholder logic)
            crm_actions = []
            if user.get('created', False):
                crm_actions.append({"action": "user_created", "user_id": mongo_user_id})
            else:
                crm_actions.append({"action": "user_found", "user_id": mongo_user_id})
            # CRM context: user info
            crm_context = {k: v for k, v in user.items() if k != '_id'}
            crm_context['user_id'] = mongo_user_id
            # If there are any ObjectIds in crm_context, convert them to strings
            for k, v in crm_context.items():
                if hasattr(v, 'binary') and hasattr(v, '__str__'):
                    crm_context[k] = str(v)
            # Step 1: Ensure conversation exists
            if not conversation_id:
                conversation = await MongoConversationService.create_conversation(mongo_user_id)
                conversation_id = str(conversation["_id"])
            else:
                conversation = await MongoConversationService.get_conversation(conversation_id)
                if not conversation:
                    conversation = await MongoConversationService.create_conversation(mongo_user_id)
                    conversation_id = str(conversation["_id"])

            # Step 2: Store user message
            await MongoMessageService.add_message(conversation_id, "user", message)

            # Step 3: Retrieve conversation history (last 10 messages)
            history = await MongoMessageService.get_messages_for_conversation(conversation_id)
            # Optionally, use history for LLM context in the future

            # Step 4: Get RAG context
            rag_context = await self.rag_agent.retrieve_context(message)

            # Step 5: Extract user info (pass only message)
            extracted_info = self.crm_agent.extract_user_info(message)
            # If new info is found, update user record
            if extracted_info:
                update_data = {k: v for k, v in extracted_info.items() if v and (not user.get(k) or user.get(k) != v)}
                if update_data:
                    await self.crm_agent.user_service.update_user(str(user["_id"]), update_data)
                    user.update(update_data)
                    crm_context.update(update_data)

            # Step 6: Generate response (simplified for now)
            if self.chat_agent:
                chat_result = self.chat_agent.process(message)
                response = chat_result["response"] if isinstance(chat_result, dict) and "response" in chat_result else str(chat_result)
            else:
                try:
                    # Build context-aware prompt
                    context_parts = []
                    
                    # Add CRM context if available
                    if crm_context:
                        if crm_context.get("name"):
                            context_parts.append(f"User name: {crm_context['name']}")
                        if crm_context.get("company"):
                            context_parts.append(f"User company: {crm_context['company']}")
                        if crm_context.get("email"):
                            context_parts.append(f"User email: {crm_context['email']}")
                        if crm_context.get("phone"):
                            context_parts.append(f"User phone: {crm_context['phone']}")
                        if crm_context.get("budget"):
                            context_parts.append(f"User budget: {crm_context['budget']}")
                        if crm_context.get("property_type"):
                            context_parts.append(f"User property preference: {crm_context['property_type']}")
                        if crm_context.get("lease_terms"):
                            context_parts.append(f"User lease terms: {', '.join(crm_context['lease_terms'])}")
                        if crm_context.get("collaboration_status"):
                            context_parts.append(f"User collaboration status: {', '.join(crm_context['collaboration_status'])}")
                    
                    # Add extracted info from current message
                    if extracted_info:
                        if extracted_info.get("lease_terms"):
                            context_parts.append(f"Current lease discussion: {', '.join(extracted_info['lease_terms'])}")
                        if extracted_info.get("collaboration_status"):
                            context_parts.append(f"Current collaboration request: {', '.join(extracted_info['collaboration_status'])}")
                    
                    # Generate context-aware response
                    if context_parts:
                        # Use context for personalized response
                        response = self._generate_meaningful_response(message, rag_context, extracted_info, crm_context)
                    else:
                        response = self._generate_meaningful_response(message, rag_context, extracted_info)
                    
                    if not response:
                        response = "I understand you're interested in real estate. How can I help you today?"
                except Exception as e:
                    self.logger.error(f"Error generating response: {e}")
                    response = "I understand you're interested in real estate. How can I help you today?"

            # Step 7: Store assistant response
            await MongoMessageService.add_message(conversation_id, "assistant", response)

            logger.info(f"Processed chat for user {mongo_user_id}: {message[:50]}...")

            # --- Expanded response fields ---
            rag_sources = rag_context if rag_context else []
            properties = []
            if rag_context:
                for item in rag_context:
                    if isinstance(item, dict):
                        if item.get('type') == 'property':
                            # Extract property details from metadata and content
                            property_details = {
                                "content": item.get("content", ""),
                                "score": item.get("score", 0.0),
                                "metadata": item.get("metadata", {}),
                                "amenities": item.get("metadata", {}).get("amenities", []),
                                "price": item.get("metadata", {}).get("price", ""),
                                "bedrooms": item.get("metadata", {}).get("bedrooms", ""),
                                "bathrooms": item.get("metadata", {}).get("bathrooms", ""),
                                "address": item.get("metadata", {}).get("address", ""),
                                "sqft": item.get("metadata", {}).get("sqft", "")
                            }
                            properties.append(property_details)
                        else:
                            # Include non-property documents as well
                            properties.append(item)
            conversation_history = history if history else []
            from datetime import datetime
            metadata = {"timestamp": datetime.utcnow().isoformat(), "model": "gpt-4-0613"}

            result = {
                "response": response,
                "user_id": mongo_user_id,
                "conversation_id": conversation_id,
                "extracted_info": extracted_info,
                "rag_sources": rag_sources,
                "crm_actions": crm_actions,
                "crm_context": crm_context,
                "properties": properties,
                "conversation_history": conversation_history,
                "metadata": metadata,
            }
            # Convert any ObjectIds in properties or conversation_history if present
            def convert_objid_in_dict(d):
                for k, v in d.items():
                    if hasattr(v, 'binary') and hasattr(v, '__str__'):
                        d[k] = str(v)
                return d
            if isinstance(result.get("properties"), list):
                result["properties"] = [convert_objid_in_dict(p) if isinstance(p, dict) else p for p in result["properties"]]
            if isinstance(result.get("conversation_history"), list):
                result["conversation_history"] = [convert_objid_in_dict(m) if isinstance(m, dict) else m for m in result["conversation_history"]]
            return result

        except Exception as e:
            self.logger.error(f"Error processing chat request: {e}")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            return {"response": "I apologize, but I encountered an error processing your request. Please try again.", "extracted_info": None}
        
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the orchestrator."""
        self.agents[agent.name] = agent
        self.logger.info(f"Registered agent: {agent.name}")
        
    def unregister_agent(self, agent_name: str) -> bool:
        """Unregister an agent. Returns True if agent was found and removed."""
        if agent_name in self.agents:
            del self.agents[agent_name]
            self.logger.info(f"Unregistered agent: {agent_name}")
            return True
        return False
        
    def define_workflow(self, name: str, agent_sequence: List[str]) -> None:
        """Define a workflow as a sequence of agent names."""
        self.workflows[name] = agent_sequence
        self.logger.info(f"Defined workflow: {name} -> {agent_sequence}")
        
    def execute_workflow(self, workflow_name: str, input_data: Any) -> Any:
        """Execute a defined workflow with input data."""
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found")
            
        workflow = self.workflows[workflow_name]
        current_data = input_data
        
        for agent_name in workflow:
            if agent_name not in self.agents:
                raise ValueError(f"Agent '{agent_name}' not found in workflow")
                
            agent = self.agents[agent_name]
            if agent.can_handle(current_data):
                current_data = agent.process(current_data)
                self.logger.info(f"Processed with agent: {agent_name}")
            else:
                self.logger.warning(f"Agent '{agent_name}' cannot handle current data")
                
        return current_data
        
    def route_request(self, input_data: Any) -> Any:
        """Route input to the most appropriate agent."""
        best_agent = None
        best_score = 0
        
        for agent in self.agents.values():
            if agent.can_handle(input_data):
                # Simple scoring - can be enhanced with more sophisticated logic
                score = len(agent.get_capabilities())
                if score > best_score:
                    best_score = score
                    best_agent = agent
                    
        if best_agent:
            return best_agent.process(input_data)
        else:
            raise ValueError("No agent can handle the input")
            
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all registered agents."""
        return {
            agent_name: agent.get_status()
            for agent_name, agent in self.agents.items()
        }
        
    def process(self, input_data: Any) -> Any:
        """Process input by routing to appropriate agent or workflow."""
        if "workflow" in self.config:
            return self.execute_workflow(self.config["workflow"], input_data)
        else:
            return self.route_request(input_data)
            
    def can_handle(self, input_data: Any) -> bool:
        """Check if orchestrator can handle input by checking if any agent can."""
        return any(agent.can_handle(input_data) for agent in self.agents.values())
        
    def get_capabilities(self) -> List[str]:
        """Get capabilities of all registered agents."""
        capabilities = []
        for agent in self.agents.values():
            capabilities.extend(agent.get_capabilities())
        return list(set(capabilities))  # Remove duplicates

    def _generate_meaningful_response(self, message: str, rag_context: List[Dict], extracted_info: Dict, crm_context: Optional[Dict] = None) -> str:
        """Generate a response based on RAG context and extracted user info. Now detects greetings and responds conversationally."""
        # Simple greeting detection
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"]
        msg_lower = message.strip().lower()
        
        # Check if this is a return conversation (user has history)
        has_history = len(rag_context) > 0 or extracted_info or crm_context
        
        if any(greet in msg_lower for greet in greetings):
            if has_history:
                # Personalized greeting for returning user
                user_name = (crm_context or {}).get("name") or extracted_info.get("name", "there")
                company = (crm_context or {}).get("company", "")
                if company:
                    return f"Hello {user_name}! Welcome back from {company}. How can I assist you with real estate today? I remember your previous interests - what would you like to explore next?"
                else:
                    return f"Hello {user_name}! Welcome back. How can I assist you with real estate today? I'm ready to help you continue your property search."
            else:
                return "Hello! How can I assist you with real estate, properties, or anything else today?"
        
        # If the message is very short or not property-related, be conversational
        if len(msg_lower) < 5:
            if has_history:
                return "Hi there! I see you're back. How can I help you with your real estate needs today?"
            else:
                return "Hi there! How can I help you with your real estate needs?"
        
        # Handle lease and collaboration requests
        if extracted_info:
            if extracted_info.get("lease_terms"):
                lease_terms = extracted_info["lease_terms"]
                return f"I see you're interested in {', '.join(lease_terms)}. I can help you find properties that match your lease requirements. Would you like me to search for available properties with these terms?"
            
            if extracted_info.get("collaboration_status"):
                collaboration = extracted_info["collaboration_status"]
                if "viewing_requested" in collaboration:
                    return "I'd be happy to help you schedule a viewing! Please provide your preferred date and time, and I'll coordinate with the property manager."
                elif "contact_requested" in collaboration:
                    return "I can help you get in touch with the property manager or agent. Would you like me to provide their contact information?"
                elif "application_ready" in collaboration:
                    return "Great! I can help you with the application process. Would you like me to guide you through the requirements and documentation needed?"
                elif "negotiation_ready" in collaboration:
                    return "I understand you're ready to make an offer or negotiate. I can help you prepare for this process. What type of property are you interested in?"
        
        # If RAG context contains property info, summarize or list them
        if rag_context and isinstance(rag_context, list) and len(rag_context) > 0:
            property_listings = [item for item in rag_context if isinstance(item, dict) and item.get('type') == 'property']
            if property_listings:
                response_parts = ["Here are some properties matching your search:"]
                
                for i, prop in enumerate(property_listings[:3]):  # Show top 3
                    content = prop.get('content', '')
                    metadata = prop.get('metadata', {})
                    
                    # Build property summary
                    summary_parts = []
                    if metadata.get('price'):
                        summary_parts.append(f"Price: {metadata['price']}")
                    if metadata.get('bedrooms'):
                        summary_parts.append(f"{metadata['bedrooms']} bedrooms")
                    if metadata.get('bathrooms'):
                        summary_parts.append(f"{metadata['bathrooms']} bathrooms")
                    if metadata.get('amenities'):
                        amenities = metadata['amenities']
                        if isinstance(amenities, list):
                            summary_parts.append(f"Amenities: {', '.join(amenities[:3])}")
                    
                    if summary_parts:
                        response_parts.append(f"• {content[:100]}... ({', '.join(summary_parts)})")
                    else:
                        response_parts.append(f"• {content[:150]}...")
                
                # Add next steps
                if has_history:
                    response_parts.append("\nWould you like me to show you more details about any of these properties, or help you schedule a viewing?")
                else:
                    response_parts.append("\nWould you like to know more about any of these properties?")
                
                return "\n\n".join(response_parts)
            else:
                # General document results
                summaries = []
                for item in rag_context[:3]:
                    if isinstance(item, dict):
                        summary = item.get('content', '')[:150]
                        summaries.append(f"• {summary}...")
                    else:
                        summaries.append(str(item))
                return "Here's what I found related to your search:\n\n" + "\n".join(summaries)
        else:
            # No RAG results, provide helpful guidance
            if has_history:
                return "I understand you're interested in real estate. Based on your previous interactions, I can help you with property searches, schedule viewings, or answer questions about the market. What would you like to explore?"
            else:
                return "I'm here to help you with real estate questions, property searches, or anything else. Please tell me what you're looking for!"


# ADD ALIAS for MCP compatibility
AgentOrchestrator = OrchestratorAgent