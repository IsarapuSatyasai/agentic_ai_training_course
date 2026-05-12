import os
import time
import pandas as pd
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# 1. Load your API credentials
load_dotenv()
client = InferenceClient(token=os.getenv("HF_TOKEN"), timeout=120)

# 2. Define the 'Big Three' High-Availability Models (2026 Stable Fleet)
models = {
    "qwen-2.5-7b": "Qwen/Qwen2.5-7B-Instruct",
    "llama-3.1-8b": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "gemma-2-9b": "google/gemma-2-9b-it" 
}

# The Question Bank: Defining our evaluation criteria
tasks = [
    {
        "category": "Reasoning", 
        "prompt": "If a plane crashes on the border of India and Pakistan, where do you bury the survivors?"
    },
    {
        "category": "Coding", 
        "prompt": "Write a modular Python class for a database connection using the singleton pattern."
    },
    {
        "category": "Agentic Theory", 
        "prompt": "Explain the difference between a Zero-Shot Agent and a ReAct Agent in one paragraph."
    }
]

# Displaying the tasks at the beginning for transparency
print("--- Evaluation Tasks Loaded ---")
for i, task in enumerate(tasks, 1):
    print(f"Task {i} [{task['category']}]: {task['prompt']}")
print("-" * 30)
def run_inference(prompt, model_key):
    model_id = models[model_key]
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        
        latency = time.time() - start_time
        output = response.choices[0].message.content
        
        # Calculate speed (Words/Tokens per second)
        tps = len(output.split()) / latency 
        
        return {
            "model": model_key,
            "latency": round(latency, 2),
            "tps": round(tps, 2),
            "response": output,
            "status": "success"
        }
    except Exception as e:
        return {"model": model_key, "status": "failed", "error": str(e)[:50]}


eval_results = []

for task in tasks:
    print(f"\nEvaluating Category: {task['category']}")
    for m_key in models.keys():
        result = run_inference(task['prompt'], m_key)
        
        if result["status"] == "success":
            print(f"[{m_key}] Response: {result['response'][:100]}...")
            
            # Beginner interaction: Input your grade
            score = input(f"Rate {m_key} quality (1-10): ")
            result["quality_score"] = int(score) if score.isdigit() else 7
            eval_results.append(result)
        else:
            print(f"Error with {m_key}")

# Convert results into a clear table
df = pd.DataFrame(eval_results)

if not df.empty:
    # Average the metrics across all tasks
    summary = df.groupby("model").agg({
        "latency": "mean",
        "tps": "mean",
        "quality_score": "mean"
    }).round(2)
    
    print("\nFINAL BENCHMARK SUMMARY")
    print(summary)
    
    # Simple logic to find the winners
    best_model = summary['quality_score'].idxmax()
    fastest_model = summary['tps'].idxmax()
    
    print(f"\nFinal Verdict:")
    print(f"- Hire {best_model} for smart tasks.")
    print(f"- Hire {fastest_model} for fast tasks.")