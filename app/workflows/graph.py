from langgraph.graph import StateGraph

from app.workflows.state import WorkflowState
from app.agents.planner_agent import PlannerAgent
from app.agents.research_agent import ResearchAgent
from app.agents.review_agent import ReviewerAgent


planner = PlannerAgent()
researcher = ResearchAgent()
reviewer = ReviewerAgent()


def planning_node(state: WorkflowState):
    plan = planner.execute(state["task"])
    return {"plan": plan}


def research_node(state: WorkflowState):
    research = researcher.execute(state["plan"])
    return {"research": research}



def review_node(state: WorkflowState):
    review = reviewer.execute(state["research"])
    return {"review": review}


builder = StateGraph(WorkflowState)

builder.add_node("planner", planning_node)
builder.add_node("researcher", research_node)
builder.add_node("reviewer", review_node)

builder.set_entry_point("planner")

builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "reviewer")

builder.set_finish_point("reviewer")

workflow = builder.compile()