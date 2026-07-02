from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from tools import add_numbers, multiply_numbers, search_web, explore_dead_letters
from config import LLM_CONFIG

load_dotenv()

def main():
    print("🚀 Tool Management System with LangChain and OpenAI")
    print("=" * 80)
    
    llm = ChatOpenAI(**LLM_CONFIG)
    tools = [add_numbers, multiply_numbers, search_web, explore_dead_letters]
    llm_with_tools = llm.bind_tools(tools)
    
    queries = [
        "Calculate 45 + 78",
        "Search for latest AI agent trends",
        "Explore dead letters in payment_queue",
        "What is 12 * 8?"
    ]
    
    for q in queries:
        print(f"\n🔍 Query: {q}")
        
        messages = [HumanMessage(content=q)]
        
        # Step 1: LLM decides which tool to call
        response = llm_with_tools.invoke(messages)
        
        if response.tool_calls:
            tool_names = [tc["name"] for tc in response.tool_calls]
            print(f"   → Tools called: {tool_names}")
            
            # Step 2: Add the Assistant's message with tool_calls
            messages.append(response)
            
            # Step 3: Execute tools
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                args = tool_call["args"]
                tool_call_id = tool_call["id"]
                
                selected_tool = next((t for t in tools if t.name == tool_name), None)
                
                if selected_tool:
                    tool_result = selected_tool.invoke(args)
                    print(f"   📊 {tool_name} Result: {tool_result}")
                    
                    # Add ToolMessage
                    messages.append(
                        ToolMessage(
                            content=str(tool_result),
                            tool_call_id=tool_call_id
                        )
                    )
            
            # Step 4: Get final response from LLM
            final_response = llm_with_tools.invoke(messages)
            print(f"   💡 Final Answer: {final_response.content}")
            
        else:
            print(f"   💡 Direct Answer: {response.content}")
        
        print("-" * 80)

if __name__ == "__main__":
    main()