from langchain_core.tools import tool
from config import ToolResult


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