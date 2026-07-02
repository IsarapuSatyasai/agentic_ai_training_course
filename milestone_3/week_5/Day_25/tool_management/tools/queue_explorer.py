from langchain_core.tools import tool
from pydantic import BaseModel, Field
from config import ToolResult
from .base import robust_tool


@tool(parse_docstring=True)
@robust_tool
def explore_dead_letters(queue_name: str, limit: int = 10) -> ToolResult:
    """Explore and summarize dead letter messages in a queue.

    Args:
        queue_name: Name of the queue to explore.
        limit: Maximum number of dead letters to inspect. Default is 10.

    Returns:
        ToolResult: Structured data containing queue stats and samples.
    
    Perfect for automation testing workflows.
    Use this to inspect failed messages, count them, and get summaries.
    """
    # Mock data for demo
    mock_dead_letters = [
        {"id": i, "error": "Timeout error", "payload_summary": "Order processing failed"}
        for i in range(min(limit, 5))
    ]
    
    return ToolResult(
        data={
            "queue": queue_name,
            "total_dead_letters": len(mock_dead_letters),
            "samples": mock_dead_letters
        },
        message=f"Explored {len(mock_dead_letters)} dead letters in {queue_name}"
    )