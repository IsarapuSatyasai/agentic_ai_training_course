import os
import time
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv() # Load API Key

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
MAX_TOKENS = 300

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    print("Error: Please set your HF_TOKEN in the .env file")
    exit(1)

client = InferenceClient(token=hf_token)

print("LLM Demo")
print("-" * 30)

#=================== HELPER FUNCTIONS ================
def count_tokens(text: str) -> int:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def generate(prompt: str, temperature: float = 0.7, max_tokens: int = MAX_TOKENS):
    start_time = time.time()

    response_object = client.chat_completion(
        model = MODEL_NAME,
        messages = [{'role':'user', 'content':prompt}],
        max_tokens = max_tokens,
        temperature = max(temperature, 0.01),
        top_p = 0.9
    )

    response_text = response_object.choices[0].message.content

    time_taken = time.time() - start_time
    input_tokens = count_tokens(prompt)
    output_tokens = count_tokens(response_text)

    return {
        "response": response_text.strip(),
        "time_taken": round(time_taken, 2),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens
    }

# ======== TEMPERATURE EXPERIMENT =========
print("1. Temperature and Probabilistic Generation")

prompt = "Write a short creative story (one paragraph) about a robot who finds a glowing flower in a desert."
temperatures = [0.1, 0.7, 1.3]

for temp in temperatures:
    print(f"\nTemperature = {temp}")
    try:
        result = generate(prompt, temperature=temp, max_tokens=100)
        print(f"Time: {result['time_taken']}s | Total Tokens: {result['total_tokens']}")
        print(result['response'])
    except Exception as e:
        print(f"Generation failed: {e}")
    print("-" * 85)

# ====================== 2. TOKENIZATION ======================
print("\n2. Tokenization Explorer")
texts = ["Hello, how are you?", "Antidisestablishmentarianism", "AI is evolving in 2026!"]

for text in texts:
    print(f"Text: {text} | Tokens: {count_tokens(text)}")

# ====================== 3. LOST IN THE MIDDLE ======================
print("\n3. Lost in the Middle Problem")

filler = "This is background data. " * 40
secret = "The secret password is PHOENIX-9247-ALPHA."
test_prompt = f"{filler}\n{secret}\n{filler}\nWhat is the secret password? Answer only with the password."

try:
    result = generate(test_prompt, temperature=0.1, max_tokens=20)
    print(f"Model Response: {result['response']}")
except Exception as e:
    print(f"Experiment failed: {e}")