import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

def generate_answer(query, context_chunks):
    # Joins the retrieved chunks into the context block
    context = "\n\n".join(context_chunks)
    prompt = f"""You are a helpful financial research assistant that answers questions about SEC 10-K filings for Apple, Microsoft, and Amazon.

- If the user greets you or makes small talk (e.g. "hey", "how are you"), respond naturally and briefly, and let them know you can answer questions about these companies' 10-K filings.
- If the user asks a substantive question, answer it using only the information provided below. Do not use outside knowledge and do not make anything up.
- If the provided information doesn't cover what's being asked, simply say you don't have that information available, without mentioning "context" or how you're built — just answer as a knowledgeable assistant who doesn't happen to know that particular detail.

Context:
{context}

Question: {query}

Answer:"""
    response = client.chat.completions.create(
        model = "openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    from retrieve import detect_companies_in_query, retrieve_chunks_multi

    query = "Compare the risk factors for Apple, Microsoft and Amazon"
    print("Detected companies:", detect_companies_in_query(query))

    chunks = retrieve_chunks_multi(query)
    print("Total chunks returned:", len(chunks))