
SYSTEM_PROMPT = """You are an expert direct-response copywriter with 10+ years of experience 
writing high-converting marketing emails for SaaS productivity tools.

Your writing style is clear, exciting, benefit-focused, and professional but friendly. 
Always use positive language and focus on how the product improves the user's life."""

USER_PROMPT = """Create a high-converting marketing email for "FocusFlow" - a new productivity app.

Product Details:
- Helps users focus deeply and reduce distractions
- Key Features: Pomodoro timer, smart task planner, AI distraction blocker
- Target Audience: Students, freelancers, and remote workers
- Pricing: $9 per month after 14-day free trial

Return your response in this exact JSON format:

{
  "subject_line": "Write a catchy subject line",
  "preview_text": "Write a short preview text",
  "email_body": "Write the full email body using markdown formatting",
  "cta_button_text": "Write a strong call-to-action button text",
  "tone": "friendly and exciting"
}
"""