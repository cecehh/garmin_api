from pydantic import BaseModel
from typing import Optional


class StepsData(BaseModel):
    date: str
    total_steps: Optional[int] = None
    step_goal: Optional[int] = None
    total_distance_meters: Optional[float] = None
