from pydantic import BaseModel
from typing import List


class Step(BaseModel):
    id: int
    title: str


class PlanResponse(BaseModel):
    steps: List[Step]