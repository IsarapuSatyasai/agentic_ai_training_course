from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class ToolResult(BaseModel):
    success: bool = True
    data: dict | list | str | None = None
    error: str | None = None

