# utils/llm.py
from __future__ import annotations
import os, openai, logging
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from dotenv import load_dotenv
load_dotenv()                       # <-- add this line

logger = logging.getLogger(__name__)

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
        timeout=REQUEST_TIMEOUT,
    )
    return resp.choices[0].message.content.strip()
