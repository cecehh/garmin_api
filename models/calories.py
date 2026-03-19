from pydantic import BaseModel
from typing import Optional


class CaloriesData(BaseModel):
    date: str
    total_kilocalories: Optional[float] = None
    active_kilocalories: Optional[float] = None
    bmr_kilocalories: Optional[float] = None
    wellness_active_kilocalories: Optional[float] = None
