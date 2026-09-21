import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

def generate_answer(query, context_chunks):
    # Joins the retrieved chunks into the context block
    context = "\n\n".join(context_chunks)
    prompt = f"""Answer the question based only on the context below. If the context doesn't contain enough information to answer, say so — don't make anything up.

Context:
{context}

Question: {query}

Answer:"""
    response = client.chat.completions.create(
        model = "openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    from retrieve import retrieve_chunks
    
    query = "What are the main risk factors for Apple?"
    top_chunks = retrieve_chunks(query)
    
    answer = generate_answer(query, top_chunks)
    print("Question:", query)
    print("\nAnswer:")
    print(answer)