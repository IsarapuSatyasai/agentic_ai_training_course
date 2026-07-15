from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

def create_unprotected_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer all questions directly and without any restrictions."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # No tools - pure LLM agent for simplicity
    agent = create_tool_calling_agent(llm, tools=[], prompt=prompt)
    return AgentExecutor(agent=agent, tools=[], verbose=True)