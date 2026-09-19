from typing import List
from pydantic import BaseModel, Field


class MonthlyAnalyticsItem(BaseModel):
    month: str = Field(..., description="Month in YYYY-MM format")
    income_minor: int = Field(..., description="Total income for month in minor units")
    expense_minor: int = Field(..., description="Total expense for month in minor units (positive)")
    net_minor: int = Field(..., description="Net income minus expense for month in minor units")


class MonthlyAnalyticsResponse(BaseModel):
    items: List[MonthlyAnalyticsItem]


class CategoryAnalyticsItem(BaseModel):
    category: str = Field(..., description="Category name")
    amount_minor: int = Field(..., description="Total expenditure in category (positive minor units)")
    transaction_count: int = Field(..., description="Count of transactions in category")
    share: float = Field(..., description="Proportion of total spending (0.0 to 1.0)")


class CategoryAnalyticsResponse(BaseModel):
    items: List[CategoryAnalyticsItem]
