from langchain_core.tools import tool

@tool
def legacy_calculate(a: float, b: float):
    """Traditional LangChain tool"""
    return a + b