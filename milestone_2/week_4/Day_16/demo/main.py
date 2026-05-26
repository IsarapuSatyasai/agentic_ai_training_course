from openai import OpenAI
from config import Config
from prompts import SYSTEM_PROMPT, USER_PROMPT
import json


def get_response():
    client = OpenAI(api_key = Config.OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ],
        temperature=Config.TEMPERATURE,
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

def main():
    print("=" * 60)
    print("Mini Research & Analysis Agent")
    print("Topic: Current State of AI Agents in 2026")
    print("=" * 60)
    print(f"Provider : {Config.PROVIDER.upper()}")
    print(f"Model    : {Config.OPENAI_MODEL if Config.PROVIDER == 'openai' else Config.HF_MODEL}")
    print("-" * 60)
    
    print("\nAgent is thinking step by step...\n")
    
    try:
        if Config.PROVIDER == "openai":
            result = get_response()
        else:
            raise NotImplementedError("Only OpenAI provider is implemented in this demo.")
        
        # Parse JSON response
        report = json.loads(result)
        
        print("\n" + "=" * 60)
        print("REPORT GENERATED SUCCESSFULLY")
        print("=" * 60)
        
        print(f"\nTitle: {report['title']}\n")
        print("Executive Summary:")
        print(report['executive_summary'])
        
        print("\nKey Trends:")
        for trend in report.get('key_trends', []):
            print(f"  • {trend}")
        
        print("\n" + "-" * 40)
        print("FULL REPORT (JSON):")
        print("-" * 40)
        print(json.dumps(report, indent=2))
        
    except Exception as e:
        print(f"\nError: {e}")
        
if __name__ == "__main__":
    main()