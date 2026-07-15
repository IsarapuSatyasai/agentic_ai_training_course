from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.state import AgentState

def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)

planner_prompt = ChatPromptTemplate.from_template(
    "You are an expert Planner agent. Break down the following task into clear, actionable steps:\n\nTask: {task}"
)

def planner_node(state: AgentState):
    llm = get_llm()
    prompt = planner_prompt.invoke({"task": state["task"]})
    response = llm.invoke(prompt)
    
    return {
        "plan": response.content,
        "messages": [response],
        "next": "researcher"
    }