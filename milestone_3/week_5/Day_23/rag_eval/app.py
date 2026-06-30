import streamlit as st
from dotenv import load_dotenv
from vector_utils import create_sample_chunks, get_vectorstore
from evaluation import create_golden_dataset, evaluate_rag

load_dotenv()

st.set_page_config(page_title="RAG Evaluation", layout="centered")
st.title("RAG Evaluation & Production Readiness")
st.markdown("**Measure • Evaluate • Improve**")

tab1, tab2, tab3 = st.tabs(["📊 Golden Dataset", "💾 Vector Store", "📈 Run Evaluation"])

with tab1:
    st.subheader("Golden Dataset")
    dataset = create_golden_dataset()
    
    for i in range(len(dataset["question"])):
        with st.expander(f"Test Case {i+1}"):
            st.write(f"**Question:** {dataset['question'][i]}")
            st.write(f"**Expected Answer:** {dataset['answer'][i]}")

with tab2:
    st.subheader("Store Test Data")
    if st.button("Store Chunks in Chroma", type="primary"):
        with st.spinner("Storing..."):
            chunks = create_sample_chunks()
            vectorstore = get_vectorstore(chunks)
            st.session_state.vectorstore = vectorstore
            st.success("✅ Data stored successfully!")

with tab3:
    st.subheader("Run RAG Evaluation")
    
    if st.button("Evaluate RAG System", type="primary"):
        if "vectorstore" not in st.session_state:
            st.error("Please store data first!")
        else:
            with st.spinner("Running Ragas Evaluation..."):
                dataset = create_golden_dataset()
                result = evaluate_rag(dataset)
                
                st.success("✅ Evaluation Completed!")
                
                # Display Results
                st.subheader("Evaluation Scores")
                for metric, score in result.scores.items():
                    st.metric(metric.replace("_", " ").title(), f"{score:.4f}")
                
                st.subheader("Detailed Results")
                st.json(result.scores)