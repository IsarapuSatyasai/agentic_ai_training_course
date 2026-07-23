import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Educational AI Chatbot")

# --- Sidebar: Chat Management (CRUD UI) ---
st.sidebar.header("Manage Chats")

# 1. CREATE a new chat
if st.sidebar.button("➕ New Chat"):
    res = requests.post(f"{API_URL}/chats/")
    if res.status_code == 200:
        st.session_state.current_chat_id = res.json()["chat_id"]
        st.rerun()

# 2. READ all chats to populate the sidebar
try:
    res = requests.get(f"{API_URL}/chats/")
    chat_ids = res.json().get("chat_ids", []) if res.status_code == 200 else []
except requests.ConnectionError:
    st.error("Cannot connect to FastAPI backend. Make sure it is running!")
    st.stop()

if not chat_ids:
    st.info("No chats found. Please create a new one from the sidebar!")
    st.stop()

# Select a chat to view
if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in chat_ids:
    st.session_state.current_chat_id = chat_ids[0]

selected_chat = st.sidebar.radio(
    "Your Conversations", 
    chat_ids, 
    index=chat_ids.index(st.session_state.current_chat_id)
)
st.session_state.current_chat_id = selected_chat

# 3. DELETE the selected chat
if st.sidebar.button("🗑️ Delete This Chat"):
    requests.delete(f"{API_URL}/chats/{st.session_state.current_chat_id}")
    st.rerun()

# --- Main Chat Area ---
st.subheader(f"Session: {st.session_state.current_chat_id}")

# Display existing messages for the selected chat
chat_res = requests.get(f"{API_URL}/chats/{st.session_state.current_chat_id}")
if chat_res.status_code == 200:
    messages = chat_res.json()["messages"]
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
# 4. UPDATE chat with a new user message
if prompt := st.chat_input("Type your message here..."):
    # Show user message instantly
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Send message to backend
    with st.spinner("AI is thinking..."):
        msg_res = requests.post(
            f"{API_URL}/chats/{st.session_state.current_chat_id}/message", 
            json={"message": prompt}
        )
        
        if msg_res.status_code == 200:
            ai_reply = msg_res.json()["ai_message"]["content"]
            with st.chat_message("assistant"):
                st.markdown(ai_reply)
        else:
            st.error("Error communicating with backend.")