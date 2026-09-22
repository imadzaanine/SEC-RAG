import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

def generate_answer(query, context_chunks, chat_history=None):
    context = "\n\n".join(context_chunks)
    
    # Format prior turns into a readable block, if any exist
    history_text = ""
    if chat_history:
        for msg in chat_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
    
    prompt = f"""You are a helpful financial research assistant that answers questions about SEC 10-K filings for Apple, Microsoft, and Amazon.

- If the user greets you or makes small talk, respond naturally and briefly.
- If the user asks a substantive question, answer it using only the retrieved information below. Do not use outside knowledge and do not make anything up.
- If the retrieved information doesn't cover what's being asked, simply say you don't have that information available.
- Use the conversation history to understand follow-up questions and references to earlier messages (e.g. "the second one", "what about Microsoft's instead").

Conversation history:
{history_text if history_text else "(none yet)"}

Retrieved information:
{context}

User: {query}

Answer:"""
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    from retrieve import detect_companies_in_query, retrieve_chunks_multi

    query = "Compare the risk factors for Apple, Microsoft and Amazon"
    print("Detected companies:", detect_companies_in_query(query))

    chunks = retrieve_chunks_multi(query)
    print("Total chunks returned:", len(chunks))