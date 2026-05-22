# main.py
from openai import OpenAI
from config import OPENAI_API_KEY
# import os
from prompts import SYSTEM_PROMPT, USER_PROMPT
import json

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)
# client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

def main():
    
    print("=== Weak Prompt Version ===")
    # Weak version (for demonstration)
    weak_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Write a marketing email for my new productivity app."}
        ],
        temperature=0.7
    )
    print(weak_response.choices[0].message.content + "...\n")  # Truncated

    print("\n" + "="*60)
    print("=== Strong Production-Grade Prompt ===")
    
    # Strong version with System + User + Structured Output
    strong_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ],
        temperature=0.5,
        response_format={"type": "json_object"}   # Force JSON output
    )
    
    # Parse and display result
    result = json.loads(strong_response.choices[0].message.content)
    
    print("\nSuccessfully Generated Marketing Email!\n")
    print(f"Subject Line : {result['subject_line']}")
    print(f"Preview Text : {result['preview_text']}")
    print(f"CTA Button   : {result['cta_button_text']}")
    print(f"Tone         : {result['tone']}\n")
    print("Email Body:")
    print(result['email_body'])

if __name__ == "__main__":
    main()