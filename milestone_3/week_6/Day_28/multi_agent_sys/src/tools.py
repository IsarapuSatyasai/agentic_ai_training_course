from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """Simple mock web search tool (No API key needed)"""
    return f"""🔍 Mock Search Results for: "{query}"

• Found several relevant articles and research papers on the topic.
• Key insights include improved reasoning, better tool usage, and autonomous workflow capabilities.
• Multiple sources confirm significant productivity gains in software development.
"""