from sentence_transformers import SentenceTransformer
import chromadb

# Load a small local model to embed the chunks of text 

model = SentenceTransformer('all-MiniLM-L6-v2')

# Set up a persistent ChromaDB client (saves to disk, not just in memory)

client = chromadb.PersistentClient(path="chroma_db")

def store_chunks(chunks, collection_name = "apple_10k"):
    collection = client.get_or_create_collection(name=collection_name)

    embeddings = model.encode(chunks).tolist()

    ids = [f"chunk_{i}" for i in range(len(chunks)) ]

    collection.add(
        ids = ids,
        embeddings = embeddings,
        documents = chunks
    )
    print(f"Stored {len(chunks)} chunks in collection '{collection_name}' ")
    return collection

if __name__ == "__main__":
    from clean import clean_html_to_text
    from chunk import chunk_text

    cleaned_text = clean_html_to_text("data/aapl_10k.htm")
    chunks = chunk_text(cleaned_text)

    store_chunks(chunks)