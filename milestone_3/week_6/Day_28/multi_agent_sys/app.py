import streamlit as st
import os
from dotenv import load_dotenv
from src.graph import build_multi_agent_graph
from src.state import AgentState

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Research System",
    layout="wide"
)

st.title("Multi-Agent Research System")
st.markdown("**LangGraph Powered • Planner → Researcher → Writer**")

# Sidebar
with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox(
        "Select LLM Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0
    )
    # st.info("Make sure your OPENAI_API_KEY and TAVILY_API_KEY are set in .env file")

# Main input
task = st.text_area(
    "Enter your research task or question:",
    placeholder="Explain the benefits and challenges of implementing Agentic AI in enterprise software development...",
    height=130
)

# Run button
if st.button("Start Multi-Agent Research", type="primary", use_container_width=True):
    if not task or not task.strip():
        st.error("Please enter a research task.")
    else:
        with st.spinner("Planner, Researcher, and Writer agents are collaborating..."):
            try:
                # Build and run the graph
                graph = build_multi_agent_graph()
                
                initial_state: AgentState = {
                    "messages": [],
                    "task": task.strip(),
                    "plan": "",
                    "research_findings": [],
                    "draft": "",
                    "feedback": "",
                    "next": ""
                }
                
                result = graph.invoke(initial_state)
                
                st.success("Multi-Agent Research Completed Successfully!")
                
                # ==================== RESULTS DISPLAY ====================
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    with st.expander("Planner Strategy & Research Findings", expanded=True):
                        st.markdown("**Task:**")
                        st.write(task.strip())
                        
                        st.markdown("**Planner's Strategy:**")
                        st.markdown(result.get("plan", "No plan generated"))
                        
                        st.markdown("**🔍 Research Findings:**")
                        findings = result.get("research_findings", [])
                        for i, finding in enumerate(findings, 1):
                            st.markdown(f"**Finding {i}:**")
                            st.markdown(finding)
                            st.divider()
                
                with col2:
                    with st.expander("Final Report by Writer Agent", expanded=True):
                        draft = result.get("draft", "No report generated")
                        st.markdown(draft)
                
                # Execution Trace
                with st.expander("Detailed Agent Execution Trace", expanded=False):
                    st.caption("See how each agent contributed step by step")
                    messages = result.get("messages", [])
                    for i, msg in enumerate(messages, 1):
                        st.write(f"**Step {i}: Agent Output**")
                        st.write(msg.content)
                        st.divider()
                        
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Make sure your `OPENAI_API_KEY` is correctly set in the `.env` file.")