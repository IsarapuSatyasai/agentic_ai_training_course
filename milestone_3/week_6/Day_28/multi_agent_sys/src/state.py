from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]      # Communication history
    task: str                                    # Original user task
    plan: str                                    # Planner's output
    research_findings: List[str]                 # Collected research
    draft: str                                   # Final report
    feedback: str                                # Critic feedback (future)
    next: str                                    # Routing decision