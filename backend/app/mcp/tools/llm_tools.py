# app/mcp/tools/llm_tools.py
"""
LLM tools for MCP - OpenAI wrapper.
Moved from utils/llm.py
"""

from __future__ import annotations
import os, openai, logging
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from dotenv import load_dotenv
load_dotenv()                       # <-- add this line

logger = logging.getLogger(__name__)

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
REQUEST_TIMEOUT = 30          # seconds

retry_policy = retry(
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(openai.APIError) |
          retry_if_exception_type(openai.RateLimitError)
)

@retry_policy
def chat(messages: list[dict]) -> str:
    """
    Send a list of OpenAI-style messages and return assistant text.
    messages = [
        {'role':'system',    'content': "..."},
        {'role':'user',      'content': "..."},
        {'role':'assistant', 'content': "..."},
        ...
    ]
    """
    logger.debug("Calling OpenAI ChatCompletion with %d messages", len(messages))
    resp = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return resp.choices[0].message.content.strip()


class LLMTools:
    """LLM tools for MCP."""
    
    def __init__(self):
        self.model = MODEL
        self.timeout = REQUEST_TIMEOUT
        
    def generate_response(self, messages: list[dict]) -> str:
        """Generate a response using the LLM."""
        return chat(messages)
        
    def generate_with_context(self, system_prompt: str, user_message: str) -> str:
        """Generate a response with system and user messages."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        return self.generate_response(messages)
        
    def generate_with_history(self, system_prompt: str, conversation_history: list[dict]) -> str:
        """Generate a response with conversation history."""
        messages = [{"role": "system", "content": system_prompt}] + conversation_history
        return self.generate_response(messages)
        
    def get_model_info(self) -> dict:
        """Get information about the current model."""
        return {
            "model": self.model,
            "timeout": self.timeout,
            "api_key_configured": bool(openai.api_key)
        } 