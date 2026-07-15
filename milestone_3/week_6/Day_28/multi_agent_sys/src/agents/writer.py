from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.state import AgentState

def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)

writer_prompt = ChatPromptTemplate.from_template(
    """You are a professional Writer agent. Create a well-structured, clear, and comprehensive final report.

Task: {task}
Research Findings: {findings}

Structure the report with clear sections."""
)

def writer_node(state: AgentState):
    llm = get_llm()
    prompt = writer_prompt.invoke({
        "task": state["task"],
        "findings": "\n\n".join(state.get("research_findings", []))
    })
    
    response = llm.invoke(prompt)
    
    return {
        "draft": response.content,
        "messages": [response],
        "next": "END"
    }