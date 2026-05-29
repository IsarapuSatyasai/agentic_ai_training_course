import streamlit as st
from src.rag_pipeline import FinancialPolicyRAG
import os

st.set_page_config(page_title="WEF Financial Policy Chatbot", layout="wide")
st.title("💰 WEF Financial Policy Chatbot")
st.markdown("Ask questions about the **Water Environment Federation Financial Policy**")

# Initialize RAG
if "rag" not in st.session_state:
    st.session_state.rag = FinancialPolicyRAG()

# Ingest PDF button (Run once)
if st.button("📥 Ingest PDF into Vector Database"):
    with st.spinner("Processing PDF..."):
        st.session_state.rag.ingest_pdf("data/wef-financial-policy.pdf")
    st.success("✅ PDF successfully loaded into vector database!")

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything about WEF Financial Policy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Retrieve
            docs, metadatas = st.session_state.rag.retrieve(prompt)
            context = "\n\n".join(docs)
            
            # Generate
            answer = st.session_state.rag.generate_answer(prompt, context)
            
            st.markdown(answer)
            
            # Show sources
            with st.expander("📑 Sources"):
                for i, (doc, meta) in enumerate(zip(docs, metadatas)):
                    st.write(f"**Page {meta['page']}**: {doc[:300]}...")

    st.session_state.messages.append({"role": "assistant", "content": answer})