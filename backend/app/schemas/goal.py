from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class GoalCreate(BaseModel):
    name: str
    target_minor: int = Field(..., gt=0)
    current_minor: int = Field(0, ge=0)
    target_date: Optional[date] = None
    currency: str = "INR"

class GoalResponse(BaseModel):
    id: int
    name: str
    target_minor: int
    current_minor: int
    target_date: Optional[date]
    progress: float
    currency: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class GoalList(BaseModel):
    items: List[GoalResponse]
