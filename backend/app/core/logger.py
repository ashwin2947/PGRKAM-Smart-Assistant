import os
import logging
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Setup standard logging to console (for immediate debugging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pgrkam_bot")

# MongoDB Setup
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "pgrkam_db")
LOG_COLLECTION = "chat_logs"

def get_db_collection():
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        return db[LOG_COLLECTION]
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB for logging: {e}")
        return None

def log_interaction(query: str, intent: str, entities: list, response: str, latency: float = 0.0):
    """
    Saves the chat interaction to MongoDB for future analysis/fine-tuning.
    Run this as a BackgroundTask so it doesn't slow down the user.
    """
    log_entry = {
        "timestamp": datetime.now(timezone.utc),
        "user_query": query,
        "predicted_intent": intent,
        "extracted_entities": entities,
        "bot_response": response,
        "latency_seconds": latency
    }

    # 1. Log to Console (So you see it happening)
    logger.info(f"📝 Logging interaction: {intent} -> {query[:30]}...")

    # 2. Log to Database (For your Research Paper dataset)
    collection = get_db_collection()
    if collection is not None:
        try:
            collection.insert_one(log_entry)
        except Exception as e:
            logger.error(f"Failed to save log to DB: {e}")