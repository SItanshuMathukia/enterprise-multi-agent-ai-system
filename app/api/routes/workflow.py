from fastapi import APIRouter
from pydantic import BaseModel

from app.workflows.master_graph import workflow

router = APIRouter()


class WorkflowRequest(BaseModel):
    task: str


@router.post("/run")
def run_workflow(request: WorkflowRequest):

    result = workflow.invoke(
        {
            "task": request.task
        }
    )

    return result