from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# Import your API routes
from app.api.endpoints import router as api_router
# Import the function to build the Keyword Index
from app.rag.retriever import initialize_bm25

# --- 1. Lifecycle Manager ---
# This runs BEFORE the app starts receiving requests
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting PGRKAM Smart Assistant...")
    
    # Initialize the BM25 (Keyword) Index from ChromaDB data
    # This ensures Hybrid Search works immediately
    try:
        initialize_bm25()
        print("✅ Search Index Initialized.")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize search index: {e}")
        
    yield
    
    print("🛑 Shutting down...")

# --- 2. App Initialization ---
app = FastAPI(
    title="PGRKAM Smart Assistant API",
    description="Backend for Multilingual Hybrid RAG Chatbot",
    version="1.0.0",
    lifespan=lifespan
)

# --- 3. CORS Policy (Crucial for Frontend connection) ---
origins = [
    "http://localhost:3000",  # React default port
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "*"                       # Allow all (for development only)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. Register Routes ---
app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router)  # Also register without prefix for frontend

# --- 5. Health Check ---
@app.get("/")
def health_check():
    return {
        "status": "online",
        "project": "PGRKAM Capstone",
        "docs_url": "http://localhost:8000/docs"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)