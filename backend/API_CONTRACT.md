# Multi-Agentic Real Estate AI API Contract

## Overview
This document describes the API contract for the backend chat system, including user/session handling, request/response formats, and best practices for frontend/backend integration.

---

## 1. /chat Endpoint

### **POST /chat**
- Accepts a user message and user/session info.
- Returns an AI response, session/user/conversation IDs, and metadata.

#### **Request Body**
```json
{
  "message": "Hi, I need office space",
  "user_id": "testuser@example.com",   // Can be email or ObjectId (string)
  "conversation_id": "<optional>"       // Optional, for multi-turn
}
```
- `user_id`: On first request, can be an email or ObjectId string. Always use the returned ObjectId for future requests.
- `conversation_id`: Optional. If omitted, a new conversation is started.

#### **Response Body**
```json
{
  "response": "...AI reply...",
  "user_id": "507f1f77bcf86cd799439011",   // Always ObjectId string
  "session_id": "507f1f77bcf86cd799439011", // Alias for user_id
  "conversation_id": "...",
  "timestamp": "2024-07-13T19:40:11.323Z",
  "processing_time": 1.23,
  "mcp_enabled": true,
  "extracted_info": { ... },
  "rag_sources": [ ... ],
  "sources": [ ... ],
  "crm_actions": [ ... ],
  "crm_context": { ... },
  "crm_data_captured": { ... },
  "properties": [ ... ],
  "conversation_history": [ ... ],
  "metadata": { ... }
}
```

---

## 2. User/Session Handling
- **First request:**
  - Send `user_id` as email (e.g., `"testuser@example.com"`).
  - Backend will create or find the user and return their MongoDB ObjectId as `user_id`/`session_id`.
- **Subsequent requests:**
  - Always use the returned ObjectId for `user_id`/`session_id`.
- **conversation_id:**
  - Omit for new conversations, or use the returned value for multi-turn context.

---

## 3. Error Handling
- **400 Bad Request:**
  - Missing required fields, invalid JSON, etc.
- **422 Unprocessable Entity:**
  - Invalid data types or schema.
- **500 Internal Server Error:**
  - Unexpected backend error. Response:
```json
{
  "detail": {
    "error": "Chat processing failed",
    "message": "...error details...",
    "processing_time": 1.23,
    "mcp_enabled": true
  }
}
```

---

## 4. Example Workflow
1. **User starts chat:**
    - Sends email as `user_id`.
2. **Receives response:**
    - Use returned `user_id` (ObjectId) for all future requests.
3. **Continues conversation:**
    - Send `conversation_id` to maintain context.

---

## 5. Best Practices
- Always use the returned `user_id`/`session_id` for all future requests.
- Store `conversation_id` if you want to maintain multi-turn context.
- Handle errors gracefully and display helpful messages to users.

---

## 6. Other Endpoints (Summary)
- `/upload_docs`: Upload documents for RAG knowledge base.
- `/crm/create_user`: Create a new user profile.
- `/crm/update_user`: Update user info by user ID.
- `/crm/conversations/{user_id}`: Get conversation history for a user.
- `/reset`: Clear conversation memory (optional).

---

For questions or integration help, contact the backend team. 