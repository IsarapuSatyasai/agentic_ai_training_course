from langchain_core.tools import tool
from pydantic import BaseModel, Field
from config import ToolResult
from .base import robust_tool


@tool(parse_docstring=True)
@robust_tool
def search_web(query: str, max_results: int = 5) -> ToolResult:
    """Search the web for information.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return. Default is 5.

    Returns:
        ToolResult: Structured results containing query and list of results.
    
    Use this tool when the user asks for current information, facts,
    or research that might require up-to-date data.
    """
    # Mock implementation - in real use, call Tavily, Serper, etc.
    mock_results = [
        {"title": f"Result 1 for {query}", "url": "https://example.com/1", "snippet": "Relevant information here..."},
        {"title": f"Result 2 for {query}", "url": "https://example.com/2", "snippet": "More details..."}
    ][:max_results]
    
    return ToolResult(
        data={"query": query, "results": mock_results},
        message=f"Found {len(mock_results)} results for '{query}'"
    )