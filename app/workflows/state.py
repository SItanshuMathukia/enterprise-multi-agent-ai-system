from typing import TypedDict, Dict, Any


class WorkflowState(TypedDict):
    task: str
    plan: Dict[str, Any]
    research: str
    review: str