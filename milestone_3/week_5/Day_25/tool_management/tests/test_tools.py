import pytest
from tools.calculator import add_numbers, multiply_numbers
from tools.search import search_web
from tools.queue_explorer import explore_dead_letters
from config import ToolResult

def test_add_numbers():
    """Test basic calculator tool."""
    result: ToolResult = add_numbers.invoke({"a": 15, "b": 27})
    assert result.success is True
    assert result.data["result"] == 42
    assert result.data["operation"] == "addition"

def test_multiply_numbers():
    """Test multiplication tool."""
    result: ToolResult = multiply_numbers.invoke({"a": 6, "b": 7})
    assert result.success is True
    assert result.data["result"] == 42

def test_search_web():
    """Test search tool with mock data."""
    result: ToolResult = search_web.invoke({"query": "LangChain agents", "max_results": 3})
    assert result.success is True
    assert len(result.data["results"]) > 0
    assert "query" in result.data

def test_queue_explorer():
    """Test queue explorer tool (relevant to automation testing)."""
    result: ToolResult = explore_dead_letters.invoke({
        "queue_name": "payment_queue", 
        "limit": 5
    })
    assert result.success is True
    assert result.data["queue"] == "payment_queue"
    assert "total_dead_letters" in result.data
    assert result.data["total_dead_letters"] >= 0

def test_error_handling():
    """Test graceful error handling in tools."""
    # This will trigger error path
    result: ToolResult = add_numbers.invoke({"a": "invalid", "b": 10})
    assert result.success is False
    assert result.error is not None