from pydantic import BaseModel

class ToolResult(BaseModel):
    success: bool = True
    data: dict | None = None
    error: str | None = None