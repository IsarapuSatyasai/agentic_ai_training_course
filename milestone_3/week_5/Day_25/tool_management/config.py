from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

class ToolResult(BaseModel):
    """Standardized response format for all tools."""
    success: bool = True
    data: dict | list | str | None = None
    error: str | None = None
    message: str | None = None
    

# LLM Configuration
LLM_CONFIG = {
    "model" : "gpt-4o-mini",
    "temperature" : 0.0
}