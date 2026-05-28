from openai import OpenAI
import streamlit as st
import json

client = OpenAI()

def analyze_ticket(ticket_text: str, model: str, temperature: float, use_self_refine: bool):
    """Optimized function with better error handling and token tracking"""
    
    from prompts.system_prompt import SYSTEM_PROMPT

    if not ticket_text.strip():
        st.warning("Ticket text cannot be empty.")
        return None, 0

    try:
        with st.spinner("Analyzing with Chain-of-Thought..."):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analyze this customer ticket:\n\n{ticket_text}"}
                ],
                temperature=temperature,
                max_tokens=900,
                response_format={"type": "json_object"}
            )

            result_text = response.choices[0].message.content
            analysis = json.loads(result_text)

            tokens_used = response.usage.total_tokens

            # Self-Refine Loop (Advanced Reasoning)
            if use_self_refine:
                with st.spinner("🔄 Self-Refining the reply..."):
                    refine_prompt = f"""Original Reply: {analysis.get('reply', '')}
Improve this reply to be more empathetic, professional, and customer-friendly."""

                    refine_response = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": refine_prompt}],
                        temperature=0.5,
                        max_tokens=400
                    )
                    analysis['reply'] = refine_response.choices[0].message.content

            return analysis, tokens_used

    except json.JSONDecodeError:
        st.error("Failed to parse JSON. The model didn't follow instructions properly.")
        return None, 0
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None, 0