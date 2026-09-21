import streamlit as st
from src.retrieve import retrieve_chunks
from src.generate import generate_answer

st.set_page_config(page_title="SEC 10-K RAG Assistant")

st.title(" SEC 10-K RAG Assistant")
st.write("Ask questions about Apple's 2025 10-K filing, answered using retrieval-augmented generation.")

query = st.text_input("Ask a question about Apple's 10-K:", placeholder="e.g. What are the main risk factors?")

if st.button("Ask") and query:
    with st.spinner("Retrieving relevant sections and generating answer..."):
        top_chunks = retrieve_chunks(query)
        answer = generate_answer(query, top_chunks)
    
    st.subheader("Answer")
    st.write(answer)
    
    with st.expander(" View source chunks used"):
        for i, chunk in enumerate(top_chunks):
            st.markdown(f"**Chunk {i+1}**")
            st.write(chunk)
            st.divider()