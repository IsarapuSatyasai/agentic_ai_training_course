from functools import wraps
import time
from config import ToolResult

def sanitize_input(text: str) -> str:
    """Basic sanitization to prevent injection attacks in tool inputs."""
    if not isinstance(text, str):
        return str(text)
    
    # Remove potential injection patterns
    dangerous = ["<script>", "DROP TABLE", "DELETE FROM", "exec("]
    
    sanitized = text
    for pattern in dangerous:
        sanitized = sanitized.replace(pattern, "[FILTERED]")
    return sanitized

def log_tool_execution(func):
    """Decorator for logging tool execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Executing tool: {func.__name__} with args: {args} kwargs: {kwargs}")
        
        result = func(*args, **kwargs)
        
        duration = time.time() - start_time
        print(f"Tool {func.__name__} executed in {duration:.2f} seconds with result: {result}")
        return result
    return wrapper

