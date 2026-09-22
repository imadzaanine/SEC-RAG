from sentence_transformers import SentenceTransformer
import chromadb

# Load a small local model to embed the chunks of text 

model = SentenceTransformer('all-MiniLM-L6-v2')

# Set up a persistent ChromaDB client (saves to disk, not just in memory)

client = chromadb.PersistentClient(path="chroma_db")

COLLECTION_NAME = "sec_filings"

def store_chunks(chunks, company_name):
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    embeddings = model.encode(chunks).tolist()

    ids = [f"chunk_{company_name}_{i}" for i in range(len(chunks)) ]

     # Metadata tags every chunk with which company it came from
    metadatas = [{"company": company_name} for _ in chunks]

    collection.add(
        ids = ids,
        embeddings = embeddings,
        documents = chunks,
        metadatas = metadatas
    )
    print(f"Stored {len(chunks)} chunks for '{company_name}' in collection '{COLLECTION_NAME}'")
    return collection

if __name__ == "__main__":
    from clean import clean_html_to_text
    from chunk import chunk_text
    from pathlib import Path

    folder = Path("data")

    for file in folder.iterdir():
        if file.is_file():
            company_name = file.stem.replace("_10k","")

            cleaned_text = clean_html_to_text(str(file))
            chunks = chunk_text(cleaned_text)

            store_chunks(chunks, company_name)