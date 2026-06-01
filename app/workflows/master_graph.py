from typing import TypedDict, Dict, Any

from langgraph.graph import StateGraph, END

from app.agents.router_agent import RouterAgent
from app.agents.coding_agent import CodingAgent
from app.agents.travel_agent import TravelAgent
from app.agents.research_agent import ResearchAgent
from app.agents.reviewer_agent import ReviewAgent
from app.agents.general_agent import GeneralAgent


# =========================
# STATE
# =========================

class WorkflowState(TypedDict, total=False):
    task: str
    route: Dict[str, Any]
    result: Dict[str, Any]


# =========================
# AGENTS
# =========================

router_agent = RouterAgent()
coding_agent = CodingAgent()
travel_agent = TravelAgent()
research_agent = ResearchAgent()
review_agent = ReviewAgent()
general_agent = GeneralAgent()


# =========================
# NODES
# =========================

def router_node(state: WorkflowState):
    route = router_agent.execute(state["task"])

    return {
        **state,
        "route": route
    }


def coding_node(state: WorkflowState):
    result = coding_agent.execute(state["task"])

    return {
        **state,
        "result": result
    }


def travel_node(state: WorkflowState):
    result = travel_agent.execute(state["task"])

    return {
        **state,
        "result": result
    }


def research_node(state: WorkflowState):
    result = research_agent.execute(state["task"])

    return {
        **state,
        "result": result
    }


def review_node(state: WorkflowState):
    result = review_agent.execute(state["task"])

    return {
        **state,
        "result": result
    }


def general_node(state):

    result = general_agent.execute(state["task"])

    return {
        "result": result
    }


# =========================
# ROUTER LOGIC
# =========================

def route_decision(state: WorkflowState):

    route = state["route"]["route"]

    if route == "coding":
        return "coding"

    elif route == "travel":
        return "travel"

    elif route == "research":
        return "research"

    elif route == "review":
        return "review"
    
    elif route == "general":
        return "general"

    return "coding"


# =========================
# BUILD GRAPH
# =========================

builder = StateGraph(WorkflowState)

# Add nodes
builder.add_node("router", router_node)
builder.add_node("coding", coding_node)
builder.add_node("travel", travel_node)
builder.add_node("research", research_node)
builder.add_node("review", review_node)
builder.add_node("general", general_node)


# Entry point
builder.set_entry_point("router")

# Conditional routing
builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "coding": "coding",
        "travel": "travel",
        "research": "research",
        "review": "review",
        "general": "general"
    }
)

# End edges
builder.add_edge("coding", END)
builder.add_edge("travel", END)
builder.add_edge("research", END)
builder.add_edge("review", END)
builder.add_edge("general", END)


# Compile workflow
workflow = builder.compile()