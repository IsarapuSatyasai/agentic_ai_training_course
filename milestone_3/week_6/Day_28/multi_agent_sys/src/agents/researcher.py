from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.state import AgentState
from src.tools import web_search

def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)

researcher_prompt = ChatPromptTemplate.from_template(
    """You are a thorough Researcher agent.

Task: {task}
Plan: {plan}
Current findings: {findings}

Use tools if needed and provide detailed research findings."""
)

def researcher_node(state: AgentState):
    llm = get_llm()
    prompt = researcher_prompt.invoke({
        "task": state["task"],
        "plan": state.get("plan", "No plan provided"),
        "findings": "\n".join(state.get("research_findings", []))
    })
    
    response = llm.invoke(prompt)
    current_findings = state.get("research_findings", []) + [response.content]
    
    return {
        "research_findings": current_findings,
        "messages": [response],
        "next": "writer"
    }