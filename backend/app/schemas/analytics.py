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


class RecurringPaymentItem(BaseModel):
    merchant_name: str = Field(..., description="Normalized merchant or payee name")
    typical_amount_minor: int = Field(..., description="Typical payment amount in minor units")
    frequency: str = Field(..., description="Detected recurrence: weekly, monthly, annual, unknown")
    next_expected_date: str = Field(..., description="Projected next billing date (YYYY-MM-DD)")
    confidence: float = Field(..., description="Detection confidence score (0.0 to 1.0)")


class RecurringAnalyticsResponse(BaseModel):
    items: List[RecurringPaymentItem]

