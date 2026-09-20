from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import (
    MonthlyAnalyticsResponse,
    CategoryAnalyticsResponse,
    RecurringAnalyticsResponse,
)
from app.schemas.budget import BudgetStatusList
from app.services.analytics_service import AnalyticsService
from app.services.recurring_service import RecurringService
from app.services.budget_service import BudgetService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/monthly", response_model=MonthlyAnalyticsResponse)
def get_monthly_analytics(
    months: int = Query(6, ge=1, le=60, description="Number of months to return"),
    db: Session = Depends(get_db),
):
    service = AnalyticsService(db)
    return service.get_monthly_analytics(user_id=1, months=months)


@router.get("/categories", response_model=CategoryAnalyticsResponse)
def get_category_analytics(
    month: Optional[str] = Query(None, description="Month in YYYY-MM format"),
    db: Session = Depends(get_db),
):
    service = AnalyticsService(db)
    return service.get_category_analytics(user_id=1, month=month)


@router.get("/recurring", response_model=RecurringAnalyticsResponse)
def get_recurring_analytics(
    db: Session = Depends(get_db),
):
    service = RecurringService(db)
    return service.detect_and_sync_recurring(user_id=1)


@router.get("/budgets", response_model=BudgetStatusList)
def get_budgets_analytics(
    month: Optional[str] = Query(None, description="Month in YYYY-MM format"),
    db: Session = Depends(get_db),
):
    service = BudgetService(db)
    return service.get_budget_status(user_id=1, month=month)

