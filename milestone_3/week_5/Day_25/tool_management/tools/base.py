from functools import wraps
from langchain_core.tools import tool
from config import ToolResult
import traceback

def robust_tool(func):
    """Decorator to add resilience to any tool."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if isinstance(result, ToolResult):
                return result
            return ToolResult(success=True, data=result)
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"Tool error: {error_msg}")
            return ToolResult(
                success=False,
                error=error_msg,
                message="Tool execution failed. Please try again or use another approach."
            )
    return wrapper
