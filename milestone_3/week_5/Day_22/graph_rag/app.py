# app.py
import streamlit as st
from dotenv import load_dotenv
from config import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP
from graph_utils import GraphDB
from vector_utils import create_chunks, get_vectorstore

load_dotenv()

st.set_page_config(page_title="Session 4: Graph RAG", layout="centered")
st.title("🚀 Session 4: Graph-Augmented RAG (G-RAG)")
st.markdown("**When Relationships Matter**")

# Sidebar
with st.sidebar:
    st.header("Settings")
    chunk_size = st.slider("Chunk Size", 200, 600, DEFAULT_CHUNK_SIZE)
    chunk_overlap = st.slider("Chunk Overlap", 0, 150, DEFAULT_CHUNK_OVERLAP)

# Load sample document
with open("sample_document.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

tab1, tab2, tab3, tab4 = st.tabs(["📄 Document", "🧠 Build Graph", "🔍 Vector vs Graph", "⚡ Hybrid Retrieval"])

with tab1:
    st.subheader("Sample Document")
    st.text_area("Content", raw_text, height=300)

with tab2:
    st.subheader("Build Knowledge Graph")
    
    if st.button("Create Sample Graph in Neo4j", type="primary"):
        with st.spinner("Connecting to Neo4j and building graph..."):
            try:
                graph_db = GraphDB()
                message = graph_db.build_sample_graph()
                graph_db.close()
                st.success(message)
            except Exception as e:
                st.error(f"Neo4j Error: {e}")
                st.info("Tip: Make sure Neo4j is running and credentials are correct in .env")

with tab3:
    st.subheader("Vector Search vs Graph Query")
    query = st.text_input("Enter your query:", "Who works on Advanced RAG System?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Vector Search"):
            if st.button("Store Chunks First", key="store1"):
                chunks = create_chunks(raw_text)
                vectorstore = get_vectorstore(chunks)
                st.session_state.vectorstore = vectorstore
                st.success("Chunks stored!")
            
            if "vectorstore" in st.session_state:
                results = st.session_state.vectorstore.similarity_search(query, k=3)
                st.write("**Vector Search Results**")
                for i, doc in enumerate(results):
                    st.write(f"{i+1}. {doc.page_content[:150]}...")

    with col2:
        if st.button("Graph Query"):
            try:
                graph_db = GraphDB()
                cypher = """
                MATCH (p:Person)-[:WORKED_ON]->(proj:Project)
                RETURN p.name as person, proj.name as project
                """
                results = graph_db.run_query(cypher)
                graph_db.close()
                
                st.write("**Graph Query Results**")
                for record in results:
                    st.write(f"Person: **{record['person']}** → Project: **{record['project']}**")
            except:
                st.error("Graph query failed. Check Neo4j connection.")

with tab4:
    st.subheader("Hybrid Vector + Graph Retrieval")
    hybrid_query = st.text_input("Hybrid Query:", "Tell me about Satyasai's work", key="hybrid")
    
    if st.button("Run Hybrid Retrieval"):
        st.info("Hybrid Retrieval = Vector Results + Graph Context")
        st.write("**This is where real production Graph RAG shines!**")
        st.caption("In full implementation, we combine both results before sending to LLM.")

st.divider()
st.caption("**Key Learning**: Use Graphs when you need relationships and multi-hop reasoning.")