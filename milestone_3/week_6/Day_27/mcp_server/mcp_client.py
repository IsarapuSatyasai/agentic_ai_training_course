from mcp_server import explore_dead_letters, DeadLetterRequest
from config import ToolResult

def call_mcp_tool(tool_name: str, **kwargs):
    """Simple MCP Client - Call tools from server"""
    if tool_name == "explore_dead_letters":
        request = DeadLetterRequest(**kwargs)
        return explore_dead_letters(request)
    raise ValueError(f"Unknown tool: {tool_name}")