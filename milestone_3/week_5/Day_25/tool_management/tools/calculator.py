from langchain_core.tools import tool
from pydantic import BaseModel, Field
from config import ToolResult
from .base import robust_tool

class CalculatorInput(BaseModel):
    """Input schema for calculator tools."""
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")


@tool(parse_docstring=True)
@robust_tool
def add_numbers(a: float, b: float) -> ToolResult:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        ToolResult: Structured result with the sum.
    
    Use this tool when you need to compute the sum of two numbers.
    """
    result = a + b
    return ToolResult(
        data={"result": result, "operation": "addition"}
    )


@tool(parse_docstring=True)
@robust_tool
def multiply_numbers(a: float, b: float) -> ToolResult:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        ToolResult: Structured result with the product.
    
    Use this for any multiplication calculations.
    """
    result = a * b
    return ToolResult(
        data={"result": result, "operation": "multiplication"}
    )