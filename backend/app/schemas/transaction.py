from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field


class TransactionItem(BaseModel):
    id: int
    date: str  # YYYY-MM-DD
    description: str
    amount_minor: int
    currency: str
    category: str


class TransactionListResponse(BaseModel):
    items: List[TransactionItem]
    page: int
    page_size: int
    total: int


class TransactionSummaryResponse(BaseModel):
    income_minor: int = Field(..., description="Total income in minor units")
    expense_minor: int = Field(..., description="Total expense in minor units (positive)")
    net_minor: int = Field(..., description="Net balance in minor units (income - expense)")
    transaction_count: int = Field(..., description="Total number of transactions in period")
    currency: str = "USD"
