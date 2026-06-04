# app.py
import streamlit as st
from dotenv import load_dotenv
from config import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP
from enrichment import load_document, enrich_chunks
from vector_db import create_vectorstore

load_dotenv()

st.set_page_config(page_title="Chunk Enrichment", layout="centered")
st.title("Chunk Enrichment & Vector Databases")
st.markdown("**Interactive Demo**")

# Sidebar
with st.sidebar:
    st.header("Settings")
    chunk_size = st.slider("Chunk Size", 200, 600, DEFAULT_CHUNK_SIZE)
    chunk_overlap = st.slider("Chunk Overlap", 0, 150, DEFAULT_CHUNK_OVERLAP)

# Load raw text
raw_text = load_document()

# Tabs
tab1, tab2, tab3 = st.tabs(["📄 Raw Document", "✨ Enrichment", "🔍 Retrieval"])

with tab1:
    st.subheader("Raw Document")
    st.text_area("Content", raw_text, height=350)

with tab2:
    st.subheader("Chunk Enrichment & Storage")
    
    if st.button("Run Enrichment & Store in Chroma", type="primary"):
        with st.spinner("Processing..."):
            chunks = enrich_chunks(raw_text, chunk_size, chunk_overlap)
            vectorstore = create_vectorstore(chunks)
            
            st.session_state.vectorstore = vectorstore
            st.session_state.chunks = chunks
            
            st.success(f"✅ {len(chunks)} enriched chunks stored in Chroma!")
            
            st.subheader("Enriched Chunks")
            for i, chunk in enumerate(chunks[:4]):   # Show first 4
                with st.expander(f"Chunk {i+1}"):
                    st.write(chunk.page_content)
                    st.json(chunk.metadata)

with tab3:
    st.subheader("Retrieval with Metadata Filter")
    
    query = st.text_input("Enter your query:", "Company expansion plans in Bangalore")
    
    if st.button("Search"):
        if "vectorstore" not in st.session_state:
            st.error("Please run enrichment first!")
        else:
            with st.spinner("Searching..."):
                results = st.session_state.vectorstore.similarity_search(
                    query, 
                    k=3,
                    filter={"category": "employee_onboarding"}
                )
                
                for i, doc in enumerate(results):
                    st.write(f"**Result {i+1}**")
                    st.write(doc.page_content)
                    st.caption(f"Metadata: {doc.metadata}")

st.divider()