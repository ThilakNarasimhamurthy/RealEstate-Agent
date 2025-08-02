import requests
import time

API_URL = "http://127.0.0.1:8000/chat"

# Initial message (user provides email, not ObjectId)
messages = [
    "Hi, I'm looking for office space in downtown for my tech startup.",
    "I'm Sarah Chen, and we need about 2000-3000 sq ft. Our budget is around $30-40 per sq ft annually.",
    "Can you show me some options with parking included?",
    "What amenities do these buildings offer?",
    "Can you arrange a viewing for Suite 402 at 123 Business Plaza?",
    "Thanks! What are the next steps if we want to proceed?"
]

user_id = "sarah.chen@example.com"  # Start with email
conversation_id = None

for i, msg in enumerate(messages):
    payload = {"message": msg, "user_id": user_id}
    if conversation_id:
        payload["conversation_id"] = conversation_id
    print(f"\n--- Turn {i+1} ---")
    print(f"User: {msg}")
    resp = requests.post(API_URL, json=payload)
    data = resp.json()
    print(f"Assistant: {data.get('response')}")
    print(f"Extracted Info: {data.get('extracted_info')}")
    print(f"CRM Data: {data.get('crm_data_captured')}")
    print(f"RAG Sources: {data.get('rag_sources')}")
    print(f"Conversation History: {data.get('conversation_history')}")
    # Use returned user_id and conversation_id for next turn
    user_id = data.get("user_id", user_id)
    conversation_id = data.get("conversation_id", conversation_id)
    time.sleep(1)  # Small delay for realism 