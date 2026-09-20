def chunk_text(text, chunk_size = 1000, overlap = 100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

if __name__ == "__main__":
    from clean import clean_html_to_text

    cleaned_text = clean_html_to_text("data/aapl_10k.htm")

    chunks = chunk_text(cleaned_text)

    print("Total chunks:", len(chunks))
    print("\nFirst chunk:")
    print(chunks[0])
    print("\nSecond chunk:")
    print(chunks[1])