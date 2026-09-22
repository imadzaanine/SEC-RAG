from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")

COLLECTION_NAME = "sec_filings"
COMPANY_NAMES = ["apple", "microsoft", "amazon"]

def retrieve_chunks(query, company=None, n_results=5):
    collection = client.get_collection(name=COLLECTION_NAME)
    
    query_embedding = model.encode([query]).tolist()
    
    # If a company is specified, filter results to just that company
    where_filter = {"company": company} if company else None
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        where=where_filter
    )
    
    return results["documents"][0]

from difflib import get_close_matches

def detect_companies_in_query(query):
    query_lower = query.lower()
    words = query_lower.split()
    
    detected = set()
    for company in COMPANY_NAMES:
        # Exact substring match (fast path)
        if company in query_lower:
            detected.add(company)
            continue
        
        # Fuzzy match against individual words in the query
        matches = get_close_matches(company, words, n=1, cutoff=0.75)
        if matches:
            detected.add(company)
    
    return list(detected)

def retrieve_chunks_multi(query, n_results_per_company=3):
    companies = detect_companies_in_query(query)
    
    if not companies:
        # No company mentioned — fall back to a general search across everything
        return retrieve_chunks(query, n_results=5)
    
    all_chunks = []
    for company in companies:
        chunks = retrieve_chunks(query, company=company, n_results=n_results_per_company)
        all_chunks.extend(chunks)
    
    return all_chunks


if __name__ == "__main__":
    # Example: search only within Apple's filing
    query = "What are the main risk factors?"
    top_chunks = retrieve_chunks(query, company="apple")
    
    for i, chunk in enumerate(top_chunks):
        print(f"--- Chunk {i+1} ---")
        print(chunk)
        print()