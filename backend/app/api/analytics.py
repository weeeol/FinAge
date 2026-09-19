from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import MonthlyAnalyticsResponse, CategoryAnalyticsResponse
from app.services.analytics_service import AnalyticsService

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
