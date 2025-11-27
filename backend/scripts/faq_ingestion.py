import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client[os.getenv("DB_NAME", "pgrkam")]
faq_collection = db["faqs"]

# Sample FAQ data
faqs = [
    {
        "question": "How to apply for government jobs in Punjab?",
        "answer": "Visit the official PGRKAM website, create an account, search for jobs, and apply online with required documents.",
        "category": "application_process"
    },
    {
        "question": "What documents are required for job application?",
        "answer": "Typically required: Aadhaar card, educational certificates, caste certificate (if applicable), income certificate, and passport-size photos.",
        "category": "documents"
    },
    {
        "question": "What is the age limit for government jobs?",
        "answer": "Age limits vary by position. Generally 18-37 years for general category, with relaxations for reserved categories.",
        "category": "eligibility"
    },
    {
        "question": "How to check application status?",
        "answer": "Login to your PGRKAM account and check the 'My Applications' section for status updates.",
        "category": "application_process"
    },
    {
        "question": "What is PGRKAM?",
        "answer": "PGRKAM (Punjab Ghar Ghar Rozgar) is Punjab government's employment portal for job seekers and employers.",
        "category": "general"
    }
]

def ingest_faqs():
    for faq in faqs:
        doc = {
            "question": faq["question"],
            "answer": faq["answer"],
            "category": faq["category"],
            "source": "faq"
        }
        
        faq_collection.update_one(
            {"question": faq["question"]},
            {"$set": doc},
            upsert=True
        )
    
    # Create text index for search
    try:
        faq_collection.create_index([("question", "text"), ("answer", "text")])
        print("Text index created for FAQs")
    except Exception:
        pass
    
    print(f"Ingested {len(faqs)} FAQs")

if __name__ == "__main__":
    ingest_faqs()