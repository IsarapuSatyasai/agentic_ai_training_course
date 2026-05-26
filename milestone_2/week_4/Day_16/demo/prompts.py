# prompts.py

SYSTEM_PROMPT = """You are an expert AI Research Analyst and Technical Writer specializing in AI Agents and Autonomous Systems.
You are highly analytical, objective, and skilled at structured reporting.
Always think step-by-step and provide well-reasoned insights."""

USER_PROMPT = """Conduct a comprehensive analysis on the current state of AI Agents in 2026.

Use Chain of Thought reasoning and break down the task into clear steps.

Return your final response in this exact JSON format:

{
  "title": "Professional report title",
  "executive_summary": "2-3 sentence summary",
  "key_trends": ["trend 1", "trend 2", "trend 3"],
  "major_developments": [
    {
      "area": "Area name",
      "description": "What happened",
      "impact": "Why it matters"
    }
  ],
  "challenges": ["challenge 1", "challenge 2"],
  "future_outlook": "Prediction for next 12-18 months",
  "conclusion": "Final thoughts"
}

Think step by step before generating the final JSON.
"""