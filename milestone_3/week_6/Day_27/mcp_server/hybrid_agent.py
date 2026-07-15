from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from mcp_client import call_mcp_tool
from legacy_tools import legacy_calculate

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def run_hybrid_demo(query: str):
    print(f"\nQuery: {query}")
    
    # Simulate tool calling
    if "dead letter" in query.lower() or "queue" in query.lower():
        result = call_mcp_tool("explore_dead_letters", queue_name="payment_queue", limit=5)
        print("MCP Tool Result:", result.data)
    else:
        result = legacy_calculate.invoke({"a": 15, "b": 27})
        print("Legacy Tool Result:", result)