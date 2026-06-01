from pydantic import BaseModel
from typing import List

class Step(BaseModel):
    id: int
    title: str
    details: str

class CodingResponse(BaseModel):
    summary: str
    steps: List[Step]
    final_output: str