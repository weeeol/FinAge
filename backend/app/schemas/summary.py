from typing import List, Literal
from pydantic import BaseModel, ConfigDict

class InsightItem(BaseModel):
    type: Literal["anomaly", "recurring", "budget", "goal"]
    title: str
    description: str
    severity: Literal["info", "warning"]

class TopCategory(BaseModel):
    category: str
    amount_minor: int

class MonthlySummaryResponse(BaseModel):
    month: str
    income_minor: int
    expense_minor: int
    net_minor: int
    top_categories: List[TopCategory]
    insights: List[InsightItem]

    model_config = ConfigDict(from_attributes=True)
