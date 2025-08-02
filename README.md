# RealEstate-Agent 🏠

## 🎯 Overview

Full-stack application that revolutionizes how real estate professionals interact with documents. Upload PDF, CSV, or TXT files, ask natural-language questions, and get GPT-4-powered answers grounded in your documents using advanced RAG (Retrieval Augmented Generation) technology.

### ✨ Key Features

- **🎨 Modern UI**: React/Next.js interface with TypeScript
- **📄 Document Processing**: Multi-format document analysis
- **🤖 AI-Powered Chat**: GPT-4 integration with conversation history
- **🔍 Smart Search**: FAISS vector-based similarity search
- **💾 Persistent Storage**: MongoDB for user data and conversations
- **⚡ Fast Response**: Sub-200ms document retrieval

---

## 🏗️ Architecture

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Next.js 15 + React 18 + TypeScript | Web interface |
| **Backend** | FastAPI + Uvicorn | API server |
| **Database** | MongoDB + Motor | Data persistence |
| **Vector Store** | FAISS | Document embeddings |
| **AI Engine** | OpenAI GPT-4 | Natural language processing |

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.8+
- MongoDB
- OpenAI API key

### Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/ThilakNarasimhamurthy/RealEstate-Agent.git
   cd RealEstate-Agent
   ```

2. **Backend setup**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Frontend setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment variables**
   
   **backend/.env:**
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   MONGODB_URL=mongodb://localhost:27017/realestate_db
   ```
   
   **frontend/.env.local:**
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

5. **Run application**
   
   **Backend (Terminal 1):**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```
   
   **Frontend (Terminal 2):**
   ```bash
   cd frontend
   npm run dev
   ```

- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`

---

## 📁 Project Structure

```
RealEstate-Agent/
├── frontend/                    # Next.js Frontend
│   ├── src/
│   │   ├── app/                # App Router
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/         # React components
│   │   │   ├── ui/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── DocumentUpload.tsx
│   │   │   └── MessageList.tsx
│   │   ├── lib/               # Utilities
│   │   │   ├── api.ts
│   │   │   └── utils.ts
│   │   └── types/             # TypeScript types
│   ├── public/               # Static assets
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── backend/                    # FastAPI Backend
│   ├── app/                   # Main application
│   │   ├── api/               # API routers
│   │   │   ├── chat.py
│   │   │   ├── crm.py
│   │   │   └── files.py
│   │   ├── core/              # Core config
│   │   │   └── database.py
│   │   ├── models/            # Data models
│   │   │   ├── user.py
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   └── services/          # Business logic
│   │       ├── embeddings.py
│   │       ├── history.py
│   │       └── crm.py
│   ├── utils/                 # Shared utilities
│   │   ├── logger.py
│   │   └── llm.py
│   ├── config/               # Configuration
│   │   └── prompt.txt
│   ├── data/                 # Data storage
│   │   ├── uploads/
│   │   └── vector_db/
│   └── requirements.txt
│
├── tests/                     # Test files
│   ├── test_conversational_chat.py
│   ├── test_crm_agent.py
│   └── test_mongo_connection.py
│
├── sample.txt
└── README.md
```

---

## 🔌 API Endpoints

### Document Management
- `POST /upload_docs` - Upload and process documents
- `GET /docs/list` - List uploaded documents

### Chat Interface
- `POST /chat` - Send message and get AI response
- `GET /chat/history/{user_id}` - Get conversation history

### User Management
- `POST /crm/create_user` - Create new user
- `PUT /crm/update_user/{id}` - Update user information
- `GET /crm/conversations/{user_id}` - Get user conversations

---

## 💡 Usage Examples

### Upload Document
```bash
curl -F "file=@contract.pdf" http://localhost:8000/upload_docs
```

### Ask Question
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"user_id": "507f1f77bcf86cd799439011", "message": "What is the earnest money?"}' \
     http://localhost:8000/chat
```

### Create User
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "agent@realty.com", "name": "John Doe", "company": "ABC Realty"}' \
     http://localhost:8000/crm/create_user
```

---

## 🛠️ Configuration

### System Prompt
Edit `backend/config/prompt.txt`:
```
You are a knowledgeable real estate assistant. Help users understand 
their documents by providing accurate, helpful information based on 
the uploaded content.
```

### Environment Variables

**Backend:**
```bash
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URL=mongodb://localhost:27017/realestate_db
LOG_LEVEL=INFO
```

**Frontend:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=RealEstate Agent
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

---


## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/name`
3. Make changes and test
4. Commit: `git commit -m 'Add feature'`
5. Push: `git push origin feature/name`
6. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) - React framework
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [MongoDB](https://mongodb.com/) - Document database
- [OpenAI](https://openai.com/) - AI models
- [FAISS](https://github.com/facebookresearch/faiss) - Vector search

---


```
