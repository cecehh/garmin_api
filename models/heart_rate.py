from pydantic import BaseModel
from typing import Optional


class HeartRateData(BaseModel):
    date: str
    average_heart_rate: Optional[int] = None
    max_heart_rate: Optional[int] = None
    resting_heart_rate: Optional[int] = None
