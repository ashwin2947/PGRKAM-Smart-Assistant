# PGRKAM Smart Assistant

A multilingual AI chatbot for Punjab Ghar Ghar Rozgar (PGRKAM) that helps users find government and private jobs, schemes, and training programs in Punjab. Supports both English and Punjabi languages with real-time translation.

## Features

- **Multilingual Support**: English and Punjabi with automatic translation
- **Job Search**: Find government and private jobs based on qualifications
- **Scheme Information**: Get details about government schemes and benefits
- **Voice Input**: Speech-to-text support for both languages
- **RAG Architecture**: Retrieval-Augmented Generation for accurate responses
- **Real-time Chat**: Fast, contextual conversations

## Architecture

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI + Python
- **AI/ML**: Sarvam AI (Chat + Translation)
- **Vector DB**: ChromaDB for job data storage
- **Database**: MongoDB for schemes, FAQs, training data
- **Search**: Hybrid search (Vector + Keyword)

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (optional, for additional data)
- Sarvam AI API Key

## Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd pgrkam-bot
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy and configure environment file:
```bash
cd backend
cp .env.example .env
# Edit .env and add your Sarvam AI API key
```

Update `backend/.env` with your credentials:
```env
SARVAM_API_KEY=your_actual_sarvam_api_key
MONGODB_URI=mongodb://localhost:27017
DB_NAME=pgrkam
```

### 4. Frontend Setup
```bash
cd chatbot-ui/web
npm install
```

## Running the Application

### Option 1: Using Startup Scripts

**Windows:**
```bash
# Run from project root
start.bat
```

**Linux/Mac:**
```bash
# Run from project root
chmod +x start.sh
./start.sh
```

### Option 2: Manual Start

**Backend:**
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
cd chatbot-ui/web
npm run dev
```

## Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Usage

1. **Open the chat interface** at http://localhost:5173
2. **Select language** using the language toggle (English/ਪੰਜਾਬੀ)
3. **Ask questions** like:
   - "Show government jobs in Punjab"
   - "I have B.Tech, find engineering jobs"
   - "What are the skill development schemes?"
4. **Use voice input** by clicking the microphone button
5. **Try example queries** from the suggestion buttons

## API Endpoints

### POST /chat
Send a chat message and get AI response.

**Request:**
```json
{
  "message": "Show government jobs in Punjab",
  "language": "en",
  "session_id": "optional-session-id",
  "history": [
    {"role": "user", "content": "previous message"},
    {"role": "assistant", "content": "previous response"}
  ]
}
```

**Response:**
```json
{
  "text": "Here are the available government jobs...",
  "session_id": "session-uuid",
  "response_id": "response-uuid",
  "original_language": "en",
  "meta": {
    "intent": "search_job",
    "processing_time": 1.23
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

## Project Structure

```
pgrkam-bot/
├── backend/
│   ├── app/
│   │   ├── api/endpoints.py      # API routes
│   │   ├── nlu/classifier.py     # Intent classification
│   │   ├── rag/
│   │   │   ├── generator.py      # Response generation
│   │   │   ├── retriever.py      # Document retrieval
│   │   │   └── vector_store.py   # Vector database
│   │   └── main.py              # FastAPI app
│   ├── requirements.txt
│   └── .env
├── chatbot-ui/web/
│   ├── src/
│   │   ├── components/
│   │   │   └── Chatbot.tsx      # Main chat interface
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── start.bat                    # Windows startup script
├── start.sh                     # Linux/Mac startup script
└── README.md
```

## Troubleshooting

### Backend Issues
- **API Key Error**: Ensure `SARVAM_API_KEY` is set in `.env`
- **Port 8000 in use**: Change port in `main.py` or kill existing process
- **Dependencies**: Run `pip install -r requirements.txt`

### Frontend Issues
- **Port 5173 in use**: Vite will automatically use next available port
- **Dependencies**: Run `npm install`
- **Build errors**: Check Node.js version (16+ required)

### Connection Issues
- **CORS errors**: Backend allows all origins in development
- **Network errors**: Ensure both servers are running
- **Translation errors**: Check Sarvam AI API key and quota

## Development

### Adding New Intents
1. Update `nlu/classifier.py` with new keywords
2. Add intent handling in `rag/generator.py`
3. Test with sample queries

### Adding New Data Sources
1. Update `rag/retriever.py` for new collections
2. Add data ingestion scripts in `scripts/`
3. Update vector store initialization

### Customizing UI
1. Modify `components/Chatbot.tsx` for interface changes
2. Update translations in the `translations` object
3. Customize styling with Tailwind classes

## License

This project is developed for Punjab Ghar Ghar Rozgar initiative.