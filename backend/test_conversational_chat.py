import requests
import time

API_URL = "http://localhost:8000/chat"
USER_ID = "test_convo_user"

# List of test messages simulating a variety of user intents
TEST_MESSAGES = [
    "hello",
    "hi there!",
    "good morning",
    "how are you?",
    "what's the weather today?",
    "I want a 2 bedroom apartment in downtown",
    "Show me office spaces with 2000 sq ft",
    "Can you help me find a house with a pool?",
    "?",
    "random text",
    "bye",
    "thank you",
    "I need a condo for rent",
    "Find me a property near Central Park",
    "Do you know any good schools nearby?",
    "What's your name?",
    "help",
    "Show me properties under $500,000",
    "",
    "goodbye"
]

def run_conversational_test():
    print("\n===== Conversational Chatbot Test =====\n")
    conversation_id = None
    for i, msg in enumerate(TEST_MESSAGES):
        payload = {"message": msg, "user_id": USER_ID}
        if conversation_id:
            payload["conversation_id"] = conversation_id
        print(f"User: {msg}")
        resp = requests.post(API_URL, json=payload)
        if resp.status_code == 200:
            data = resp.json()
            print(f"Assistant: {data.get('response')}")
            conversation_id = data.get("conversation_id", conversation_id)
        else:
            print(f"Assistant: [Error {resp.status_code}] {resp.text}")
        print("-" * 60)
        time.sleep(0.5)  # Small delay for readability
    print("\n===== End of Test =====\n")

if __name__ == "__main__":
    run_conversational_test() 