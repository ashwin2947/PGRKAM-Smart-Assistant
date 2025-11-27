from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time
import uuid
from datetime import datetime
# Import our custom services (The "Brain" modules)
from app.nlu.classifier import predict_intent
# from app.nlu.entity_extractor import extract_entities
from app.rag.retriever import hybrid_search
from app.rag.generator import generate_response
from app.core.logger import log_interaction
from sarvamai import SarvamAI
import os
from dotenv import load_dotenv

load_dotenv()
client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text using Sarvam AI"""
    try:
        response = client.text.translate(
            input=text,
            source_language_code=source_lang,
            target_language_code=target_lang,
            mode="formal",
            model="sarvam-translate:v1",
            numerals_format="native",
            speaker_gender="Male",
            enable_preprocessing=False
        )
        return response.translated_text
    except AttributeError:
        print(f"Translation API not available, returning original text")
        return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

router = APIRouter()

# --- 1. Data Models ---
class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    session_id: Optional[str] = None
    history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    text: str
    session_id: str
    response_id: str
    original_language: str
    meta: Optional[Dict[str, Any]] = None
    timestamp: str

# --- 2. The Chat Logic ---
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest, background_tasks: BackgroundTasks):
    start_time = time.time()
    """
    Multilingual Chat Pipeline: NLU -> Retrieval -> Generation -> Response
    """
    try:
        # Generate session and response IDs
        session_id = payload.session_id or str(uuid.uuid4())
        response_id = str(uuid.uuid4())
        
        # Translation workflow for Punjabi
        query_for_processing = payload.message
        if payload.language == "pa":
            # Translate Punjabi to English for processing
            query_for_processing = translate_text(payload.message, "pa-IN", "en-IN")
            print(f"Translated query: {query_for_processing}")
        
        # Step 1: NLU Layer (always in English)
        intent = predict_intent(query_for_processing)
        entities = []  # Simplified for now
        
        # Step 2: Retrieval Layer (always in English)
        top_docs = hybrid_search(query_for_processing, top_k=3)
        
        # Step 3: Generation (always in English first)
        english_response = generate_response(
            query=query_for_processing, 
            context_docs=top_docs,
            intent=intent,
            language="en",  # Always generate in English first
            history=payload.history
        )
        
        # Step 4: Translate response back to Punjabi if needed
        final_answer = english_response
        if payload.language == "pa":
            final_answer = translate_text(english_response, "en-IN", "pa-IN")
            print(f"Translated response: {final_answer}")
        
        process_time = time.time() - start_time
        
        # Step 4: Logging (Background Task)
        # background_tasks.add_task(
        #     log_interaction, 
        #     query=payload.message, 
        #     intent=intent, 
        #     entities=entities, 
        #     response=final_answer,
        #     latency=process_time
        # )
        
        return ChatResponse(
            text=final_answer,
            session_id=session_id,
            response_id=response_id,
            original_language=payload.language,
            meta={
                "intent": intent,
                "entities": entities,
                "sources": [doc['source'] for doc in top_docs],
                "processing_time": process_time,
                "translated_query": query_for_processing if payload.language == "pa" else None
            },
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))