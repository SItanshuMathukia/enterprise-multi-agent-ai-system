from pydantic import BaseModel
from typing import List


class TravelStep(BaseModel):
    id: int
    title: str
    details: str


class TravelResponse(BaseModel):
    summary: str
    steps: List[TravelStep]
    booking_flow: str