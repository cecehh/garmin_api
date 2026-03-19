from pydantic import BaseModel
from typing import Optional


class DailyStats(BaseModel):
    date: str
    total_steps: Optional[int] = None
    step_goal: Optional[int] = None
    total_distance_meters: Optional[float] = None
    total_kilocalories: Optional[float] = None
    active_kilocalories: Optional[float] = None
    bmr_kilocalories: Optional[float] = None
    wellness_active_kilocalories: Optional[float] = None
    average_heart_rate: Optional[int] = None
    max_heart_rate: Optional[int] = None
    resting_heart_rate: Optional[int] = None
    average_stress_level: Optional[int] = None
    floor_climbed: Optional[int] = None
    minutes_sedentary: Optional[int] = None
    minutes_lightly_active: Optional[int] = None
    minutes_moderately_active: Optional[int] = None
    minutes_highly_active: Optional[int] = None
