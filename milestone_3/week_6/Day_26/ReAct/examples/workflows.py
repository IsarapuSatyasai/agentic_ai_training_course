from agents.react_agent import agent_executor

def run_workflow(query: str):
    print(f"\n Query: {query}")
    result = agent_executor.invoke({"input": query})
    print(f"Final Answer: {result['output']}")
    return result


    