from langchain_core.tools import tool
from config import ToolResult

@tool(parse_docstring=True)
def calculate(expression: str) -> ToolResult:
    """Perform basic arithmetic calculations.
    
    Args:
        expression: A simple arithmetic expression like "45 + 78", "10 * 5", "100 / 4", etc.
    
    Returns:
        ToolResult: The result of the calculation.
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {"pow": pow})
        return ToolResult(data={
            "result": float(result), 
            "operation": "calculation",
            "expression": expression
        })
    except Exception as e:
        return ToolResult(data={"error": str(e)})


@tool(parse_docstring=True)
def search_web(query: str, max_results: int = 3) -> ToolResult:
    """Search the web for the given query.
    
    Args:
        query: The search query string.
        max_results: Maximum number of results to return. Defaults to 3.
    
    Returns:
        ToolResult: Search results.
    """
    return ToolResult(data={
        "query": query,
        "result": [f"Result {i} for {query}" for i in range(max_results)]
    })


@tool(parse_docstring=True)
def explore_dead_letters(queue_name: str, limit: int = 5) -> ToolResult:
    """Explore dead letter messages in a queue.
    
    Useful for debugging failed messages (e.g., during automation testing).
    
    Args:
        queue_name: Name of the queue to inspect.
        limit: Maximum number of dead letter samples to return. Defaults to 5.
    
    Returns:
        ToolResult: Queue info and sample messages.
    """
    mock_data = [
        {"id": f"dl={i}", "error": "Timeout", "payload": "Failed order"}
        for i in range(min(limit, 4))
    ]
    return ToolResult(data={
        "queue": queue_name,
        "total": len(mock_data),
        "samples": mock_data
    })