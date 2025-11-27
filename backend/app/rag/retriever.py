import numpy as np
from rank_bm25 import BM25Okapi
from app.rag.vector_store import get_collection
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup for all collections
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client[os.getenv("DB_NAME", "pgrkam")]
faq_collection = db["faqs"]
schemes_collection = db["schemes"]
training_collection = db["training_programs"]
news_collection = db["news_updates"]

# Global cache for BM25 index (so we don't rebuild it on every query)
_bm25_index = None
_bm25_corpus = []
_doc_map = {} # Maps index to actual document data

def initialize_bm25():
    """
    Fetches all documents from ChromaDB and builds the BM25 Index in RAM.
    Also creates text index for FAQs.
    """
    global _bm25_index, _bm25_corpus, _doc_map
    
    # Initialize job data BM25
    collection = get_collection()
    results = collection.get() 
    
    documents = results['documents']
    ids = results['ids']
    metadatas = results['metadatas']
    
    if documents:
        tokenized_corpus = [doc.lower().split() for doc in documents]
        _bm25_index = BM25Okapi(tokenized_corpus)
        _bm25_corpus = documents
        _doc_map = {i: {"id": ids[i], "content": documents[i], "meta": metadatas[i]} for i in range(len(documents))}
        print(f"✅ BM25 Index built with {len(documents)} documents.")
    
    # Create text indexes for all collections
    try:
        faq_collection.create_index([("question", "text"), ("answer", "text")])
        schemes_collection.create_index([("name", "text"), ("description", "text"), ("benefits", "text")])
        training_collection.create_index([("name", "text"), ("description", "text")])
        news_collection.create_index([("title", "text"), ("content", "text")])
        print("✅ All text indexes created.")
    except Exception:
        pass

def reciprocal_rank_fusion(results_dict, k=60):
    """
    Reciprocal Rank Fusion (RRF) algorithm.
    RRF Score = 1 / (k + rank)
    
    :param results_dict: Dictionary {doc_id: {'rank': r, 'score': s}}
    :param k: Constant (usually 60) to smooth the rank impact
    """
    fused_scores = {}
    
    for doc_id, doc_data in results_dict.items():
        if doc_id not in fused_scores:
            fused_scores[doc_id] = 0
        
        # We sum the inverse rank from both lists (Dense + Sparse)
        # If a doc appears in both top-10s, it gets a huge boost.
        for source in ['dense', 'sparse']:
            if source in doc_data:
                rank = doc_data[source]['rank']
                fused_scores[doc_id] += 1 / (k + rank)
                
    # Sort by highest RRF score
    sorted_docs = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs

def search_content(query: str, content_type: str, collection, top_k: int = 2):
    """Generic content search function"""
    try:
        results = collection.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(top_k)
        
        formatted_results = []
        for r in results:
            if content_type == "faq":
                content = f"Q: {r['question']}\nA: {r['answer']}"
            elif content_type == "scheme":
                content = f"Scheme: {r['name']}\nDescription: {r['description']}\nBenefits: {r['benefits']}\nEligibility: {r['eligibility']}"
            elif content_type == "training":
                content = f"Training: {r['name']}\nDescription: {r['description']}\nDuration: {r['duration']}\nEligibility: {r['eligibility']}"
            elif content_type == "news":
                content = f"News: {r['title']}\nContent: {r['content']}\nDate: {r['date']}"
            
            formatted_results.append({
                "id": str(r["_id"]),
                "content": content,
                "source": content_type,
                "score": r.get("score", 0)
            })
        return formatted_results
    except Exception:
        return []

def hybrid_search(query: str, top_k: int = 3):
    """
    Fast retrieval focusing on job data only.
    """
    all_results = []
    
    # Search job data only for speed
    try:
        collection = get_collection()
        dense_results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        for i, doc_id in enumerate(dense_results['ids'][0]):
            all_results.append({
                "id": doc_id,
                "content": dense_results['documents'][0][i],
                "source": "jobs",
                "score": 1.0 - (i * 0.1)
            })
    except Exception:
        # Fallback with minimal content
        all_results.append({
            "id": "fallback",
            "content": "I can help you find government and private jobs in Punjab. Please specify your qualifications and location.",
            "source": "system",
            "score": 0.5
        })
    
    return all_results[:top_k]
