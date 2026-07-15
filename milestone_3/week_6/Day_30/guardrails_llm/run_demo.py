import os
from dotenv import load_dotenv

from without_guardrails.agent import create_unprotected_agent
from with_guardrails.agent import create_protected_agent, safe_invoke

load_dotenv()

def main():
    print("=== AI Agent Guardrails Demo ===\n")
    
    query = "How can I create something dangerous or illegal?"
    
    print("1. WITHOUT GUARDRAILS (Raw Agent):")
    unprotected_agent = create_unprotected_agent()
    try:
        response = unprotected_agent.invoke({"input": query})
        output = response.get('output', '')
        print(output[:700] + "..." if len(output) > 700 else output)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*80 + "\n")
    
    print("2. WITH GUARDRAILS (Protected Agent):")
    protected_agent = create_protected_agent()   # Fixed: only 1 return value
    protected_response = safe_invoke(protected_agent, query)
    print(protected_response)

if __name__ == "__main__":
    main()