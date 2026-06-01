from pydantic import BaseModel
from typing import Literal


class RouterResponse(BaseModel):
    route: Literal["coding", "research", "review", "planning", "travel", "general"]
    confidence: float | None = None
    reasoning: str | None = None