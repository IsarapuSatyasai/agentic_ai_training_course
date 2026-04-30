import os
import json
import requests
from dotenv import load_dotenv
from tools import available_tools  # Ensure your tools.py is updated with the 5 tools

# Load Environment Variables
load_dotenv()

class AutonomousAgent:
    def __init__(self, model="gpt-4"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.url = "https://api.openai.com/v1/chat/completions"
        
        # Enhanced System Prompt to prevent tool name/argument errors
        self.system_prompt = (
            "You are a helpful AI Agent with access to tools. "
            "If you need to use a tool, you MUST respond in JSON format: "
            '{"tool": "function_name", "args": [arg1, arg2]}. '
            f"Available tools: {list(available_tools.keys())}. "
            "Notes: 'convert_currency' takes [amount, from_code, to_code]. "
            "If no tool is needed, respond with plain text."
        )
        
        self.memory = [{"role": "system", "content": self.system_prompt}]

    def _call_llm(self, message, role="user"):
        """Internal method to talk to OpenAI."""
        self.memory.append({"role": role, "content": message})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": self.memory,
            "temperature": 0  # Low temperature for consistent tool calling
        }

        try:
            response = requests.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            
            # Store assistant response in memory
            self.memory.append({"role": "assistant", "content": content})
            return content
        except Exception as e:
            return f"Error: {e}"

    def run(self, task):
        """The main loop: Think -> Act -> Observe -> Final Response."""
        # 1. THINK: Send user task to LLM
        llm_response = self._call_llm(task)
        
        # 2. ACT: Check if the response is a JSON tool call
        try:
            # We check if the response looks like JSON
            if '{"tool"' in llm_response.replace(" ", ""):
                # Clean the response string in case LLM added markdown triple backticks
                clean_json = llm_response.replace("```json", "").replace("```", "").strip()
                action = json.loads(clean_json)
                
                tool_name = action['tool']
                args = action.get('args', [])

                # Validate tool existence
                if tool_name in available_tools:
                    print(f"[*] Executing Tool: {tool_name} with {args}")
                    
                    # Execute the tool from tools.py
                    observation = available_tools[tool_name](*args)
                    print(f"[*] Observation: {observation}")

                    # 3. OBSERVE: Send tool results back to LLM for a final summary
                    final_reply = self._call_llm(
                        f"The tool '{tool_name}' returned: {observation}. "
                        "Based on this, give the user a clear final answer.",
                        role="user"
                    )
                    return final_reply
                else:
                    return f"Agent tried to use unknown tool: {tool_name}"

        except (json.JSONDecodeError, TypeError) as e:
            # If JSON is malformed or tool arguments are wrong, return the raw response
            return llm_response

        # If it wasn't a tool call, just return the text
        return llm_response

# --- Interactive Session ---
if __name__ == "__main__":
    bot = AutonomousAgent()
    print("--- Agent Online (Type 'exit' to stop) ---")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        
        answer = bot.run(user_input)
        print(f"\nAgent: {answer}\n")