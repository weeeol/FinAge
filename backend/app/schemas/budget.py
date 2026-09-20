from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class BudgetCreate(BaseModel):
    category: str
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$")
    limit_minor: int = Field(..., ge=0)
    currency: str = "INR"

class BudgetResponse(BaseModel):
    id: int
    category: str
    month: str
    limit_minor: int
    currency: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BudgetStatus(BaseModel):
    budget_id: int
    category: str
    limit_minor: int
    spent_minor: int
    remaining_minor: int
    percent_used: float
    status: str

class BudgetStatusList(BaseModel):
    items: List[BudgetStatus]
