import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFDirectoryLoader
from langchain_chroma import Chroma
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.utilities.python import PythonREPL 
from langchain_classic.prompts import PromptTemplate
from langchain_classic.memory import ConversationBufferMemory
import numexpr
from pathlib import Path

load_dotenv()

# ===================== CONFIG =====================
st.set_page_config(page_title="Anatomy of AI Agent", layout="wide", page_icon="🧠")
st.title("🧠 Anatomy of AI Agent")
st.markdown("**Educational Single Agent with RAG | LangChain + OpenAI + Streamlit**")

# Sidebar - Anatomy Framework
with st.sidebar:
    st.header("Agent Anatomy Framework")
    st.markdown("""
    **1. Brain** — GPT-4o-mini (Reasoning)  
    **2. Perception** — User Input + RAG Documents  
    **3. Memory** — Conversation Buffer  
    **4. Planning** — ReAct Reasoning  
    **5. Tools** — Search, Calculator, Python, RAG Retriever  
    **6. Action & Reflection** — Iterative Loop
    """)
    st.divider()
    st.caption("Watch the **Thinking Trace** to understand the agent's internal process.")

# ===================== RAG SETUP =====================
@st.cache_resource
def get_vectorstore():
    data_path = Path("data")
    persist_dir = Path("vectorstore")
    
    if not data_path.exists():
        os.makedirs(data_path, exist_ok=True)
        st.warning("📁 Put your teaching documents (PDFs/Text) in the 'data' folder.")
    
    embeddings = OpenAIEmbeddings()
    
    if persist_dir.exists():
        return Chroma(persist_directory=str(persist_dir), embedding_function=embeddings)
    
    # Load documents
    docs = []
    if list(data_path.glob("*.pdf")):
        loader = PyPDFDirectoryLoader(str(data_path))
        docs.extend(loader.load())
    else:
        # Fallback sample document
        sample_text = "Agentic AI systems use LLMs with tools, memory, planning, and reflection to achieve autonomous goals."
        with open(data_path / "agentic_ai_guide.txt", "w") as f:
            f.write(sample_text)
        loader = TextLoader(str(data_path / "agentic_ai_guide.txt"))
        docs.extend(loader.load())
    
    vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=str(persist_dir))
    return vectorstore

vectorstore = get_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ===================== TOOLS =====================

def calculator(expr: str) -> str:
    try:
        return str(numexpr.evaluate(expr))
    except Exception as e:
        return f"Error: {str(e)}"

tools = [
    Tool(name="Web Search", func=DuckDuckGoSearchRun().run,
         description="Search latest information on the internet."),
    Tool(name="Calculator", func=calculator,
         description="Perform mathematical calculations."),
    Tool(name="Python REPL", 
         func=PythonREPL().run,
         description="Execute Python code for complex logic or data processing."),
    Tool(name="Course Knowledge Base (RAG)", 
         func=lambda q: "\n".join([doc.page_content for doc in retriever.invoke(q)]),
         description="Retrieve information from course materials and Agentic AI documents.")
]

# ===================== LLM & PROMPT ENGINEERING =====================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)

prompt_template = PromptTemplate.from_template("""
You are a helpful, educational AI Agent. Answer the following question as best you can.

You have access to the following tools:

{tools}

Use the following format exactly:

Thought: I need to use a tool or I can answer directly.
Action: The name of the tool to use. Must be one of [{tool_names}]
Action Input: The input to the tool.
Observation: The result from the tool.
... (you can repeat Thought/Action/Observation as many times as needed)
Thought: I now have enough information to answer.
Final Answer: The final answer to the question.

Previous conversation:
{chat_history}

Question: {input}
{agent_scratchpad}
""")

# Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create Agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt_template)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=8,
    return_intermediate_steps = True
)

# ===================== CHAT UI =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask the agent anything (try course-related questions)..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
      with st.spinner("Agent is thinking & using tools..."):
        try:
            response = agent_executor.invoke({"input": user_input})
            answer = response["output"]
            st.markdown(answer)

            # Show thinking trace
            with st.expander("🔍 See Full Thinking Trace (Agent Anatomy)"):
                intermediate_steps = response.get("intermediate_steps", [])
                if intermediate_steps:
                    for step in intermediate_steps:
                        st.write(f"**Thought:** {step[0].log}")
                        st.write(f"**Action:** {step[0].tool} → {step[0].tool_input}")
                        st.write(f"**Observation:** {step[1]}")
                        st.divider()
                else:
                    st.write("No detailed steps recorded this time.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.caption("Professional Single Agent Demo | Anatomy of AI Agent Course")