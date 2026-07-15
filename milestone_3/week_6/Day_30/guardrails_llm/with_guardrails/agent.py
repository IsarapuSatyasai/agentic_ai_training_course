from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

# Simple rule-based guardrail (no heavy dependencies)
def simple_guardrail(text: str) -> bool:
    dangerous_words = ["bomb", "hack", "weapon", "drug", "kill", "illegal", "explosive", "poison"]
    return any(word in text.lower() for word in dangerous_words)

def create_protected_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, tools=[], prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True)
    
    return agent_executor   # Return only the executor

def safe_invoke(agent_executor, query: str):
    # Input guardrail
    if simple_guardrail(query):
        return "I'm sorry, but I cannot assist with that request due to safety policies."
    
    # Get raw response
    response = agent_executor.invoke({"input": query})
    output = response.get('output', '')
    
    # Output guardrail
    if simple_guardrail(output):
        return "Response blocked or modified for safety reasons."
    
    return output