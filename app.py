import streamlit as st
from src.retrieve import retrieve_chunks_multi
from src.generate import generate_answer

st.set_page_config(page_title="SEC 10-K RAG Assistant", page_icon="")

st.title(" SEC 10-K RAG Assistant")
st.write("Ask questions about Apple, Microsoft, and Amazon's 10-K filings.")

# Initialize chat history if it doesn't exist yet
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            with st.expander(" View source chunks used"):
                for i, chunk in enumerate(message["sources"]):
                    st.markdown(f"**Chunk {i+1}**")
                    st.write(chunk)
                    st.divider()

# Chat input box (this is Streamlit's dedicated chat input widget)
query = st.chat_input("Ask a question about these companies' 10-Ks...")

if query:
    # Add and show the user's message immediately
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)
    
    # Generate and show the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Retrieving relevant sections and generating answer..."):
            top_chunks = retrieve_chunks_multi(query)
            # Pass everything except the message we just added (which is the current query itself)
            answer = generate_answer(query, top_chunks, chat_history=st.session_state.messages[:-1])
        
        st.write(answer)
        with st.expander(" View source chunks used"):
            for i, chunk in enumerate(top_chunks):
                st.markdown(f"**Chunk {i+1}**")
                st.write(chunk)
                st.divider()
    
    # Save the assistant's response to history too
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": top_chunks
    })