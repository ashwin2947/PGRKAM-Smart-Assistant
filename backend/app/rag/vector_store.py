import chromadb
from chromadb.utils import embedding_functions
import os

# Use a local folder for the database
PERSIST_DIRECTORY = "./data/vector_db"

# Initialize ChromaDB Client
client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)

# Use BAAI/bge-m3 (or a smaller alternative like all-MiniLM-L6-v2 for speed)
# We use the default SentenceTransformer embedding function provided by Chroma
emb_fn = embedding_functions.DefaultEmbeddingFunction()

def get_collection():
    """
    Returns the ChromaDB collection for PGRKAM documents.
    Creates it if it doesn't exist.
    """
    return client.get_or_create_collection(
        name="pgrkam_docs",
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"} # Cosine similarity is best for text
    )

def add_documents(documents: list, metadatas: list, ids: list):
    """
    Adds text chunks to the vector database.
    """
    collection = get_collection()
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )