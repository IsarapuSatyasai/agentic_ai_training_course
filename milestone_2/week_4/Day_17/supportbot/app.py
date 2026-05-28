import streamlit as st
from config import MODELS
from core.llm_handler import analyze_ticket

# Page Config
st.set_page_config(page_title="TicketHelper", page_icon="🎫", layout="wide")

st.title("🎫 TicketHelper")

# Sidebar Controls
with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox("Select Model", options=list(MODELS.keys()))
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.05)
    use_refine = st.checkbox("Enable Self-Refine", value=True)
    
    st.divider()
    st.caption("Concepts Demonstrated:")
    st.caption("• COSTAR Prompting\n• Chain-of-Thought\n• Self-Refine\n• Structured JSON Output\n• Model Selection")

# Main Input
ticket = st.text_area(
    "Paste Customer Support Ticket",
    height=220,
    placeholder="Enter the customer's message here..."
)

# Analyze Button
if st.button("🚀 Analyze Ticket", type="primary", use_container_width=True):
    if ticket.strip():
        result, tokens = analyze_ticket(ticket, model_name, temperature, use_refine)
        
        if result:
            st.success("✅ Analysis Completed Successfully!")

            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Category", result.get("category", "N/A"))
            with col2:
                st.metric("Priority", result.get("priority", "N/A"))
            with col3:
                st.metric("Tokens Used", f"{tokens:,}")

            # Results
            st.subheader("📝 Summary")
            st.write(result.get("summary", "No summary available"))

            st.subheader("💬 Professional Reply")
            st.write(result.get("reply", "No reply generated"))

            with st.expander("🔍 Chain of Thought (Reasoning)"):
                st.write(result.get("reasoning", "No reasoning available"))

            with st.expander("📦 Full JSON Output"):
                st.json(result)
    else:
        st.warning("Please enter a customer ticket.")