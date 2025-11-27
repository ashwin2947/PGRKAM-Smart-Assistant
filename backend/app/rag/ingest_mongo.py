# backend/app/rag/ingest_mongo.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from app.rag.vector_store import add_documents

# Load environment variables
load_dotenv()

# Configuration (Match these with your scraper's .env)
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "pgrkam_db") # Default if not set
COLL_PRIVATE = os.getenv("COLL_PRIVATE", "private_jobs")
COLL_GOVT = os.getenv("COLL_GOVT", "govt_jobs")

def format_job_to_text(job: dict, job_type: str) -> str:
    """
    Converts a JSON job record into a readable text chunk for the LLM.
    """
    # Base fields
    text = f"JOB_TYPE: {job_type}\n"
    text += f"ROLE: {job.get('name_of_post', 'N/A')}\n"
    text += f"ORGANIZATION: {job.get('name_of_employer', 'N/A')}\n"
    text += f"LOCATION: {job.get('place_of_posting', 'N/A')}\n"
    text += f"QUALIFICATION: {job.get('required_qualification', 'N/A')}\n"
    
    # Specific fields
    if job_type == "Government":
        text += f"DEADLINE: {job.get('last_apply_date', 'N/A')}\n"
        text += f"AGE LIMIT: {job.get('maximum_applicable_age', 'N/A')}\n"
        text += f"OFFICIAL NOTIFICATION: {job.get('notification_link', 'N/A')}\n"
    else:
        text += f"SALARY: {job.get('salary', 'N/A')}\n"
        text += f"VACANCIES: {job.get('vacancies', 'N/A')}\n"

    # Common fields
    text += f"APPLY LINK: {job.get('apply_link', 'N/A')}\n"
    
    return text

def ingest_from_mongo():
    print("🚀 Connecting to MongoDB to fetch jobs...")
    
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        
        documents = []
        metadatas = []
        ids = []
        
        # 1. Fetch Private Jobs
        private_cursor = db[COLL_PRIVATE].find()
        count_p = 0
        for job in private_cursor:
            text_chunk = format_job_to_text(job, "Private Sector")
            doc_id = str(job["_id"])
            
            documents.append(text_chunk)
            metadatas.append({
                "source": "pgrkam_private", 
                "job_id": doc_id, 
                "type": "private"
            })
            ids.append(doc_id)
            count_p += 1
            
        # 2. Fetch Govt Jobs
        govt_cursor = db[COLL_GOVT].find()
        count_g = 0
        for job in govt_cursor:
            text_chunk = format_job_to_text(job, "Government")
            doc_id = str(job["_id"])
            
            documents.append(text_chunk)
            metadatas.append({
                "source": "pgrkam_govt", 
                "job_id": doc_id,
                "type": "govt"
            })
            ids.append(doc_id)
            count_g += 1

        if not documents:
            print("⚠️ No jobs found in MongoDB. Did you run the scraper?")
            return

        print(f"📦 Found {count_p} Private and {count_g} Govt jobs.")
        
        # 3. Batch Insert into ChromaDB
        # We process in batches of 100 to be safe
        BATCH_SIZE = 100
        for i in range(0, len(documents), BATCH_SIZE):
            batch_docs = documents[i:i+BATCH_SIZE]
            batch_meta = metadatas[i:i+BATCH_SIZE]
            batch_ids = ids[i:i+BATCH_SIZE]
            
            add_documents(batch_docs, batch_meta, batch_ids)
            print(f"   Processed batch {i} to {i+len(batch_docs)}")

        print("🎉 Successfully synced MongoDB to ChromaDB!")

    except Exception as e:
        print(f"❌ Error during ingestion: {e}")

if __name__ == "__main__":
    ingest_from_mongo()