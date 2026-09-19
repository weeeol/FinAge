from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.transaction import TransactionListResponse, TransactionSummaryResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=TransactionListResponse)
def list_transactions(
    from_date: Optional[date] = Query(None, description="Start date YYYY-MM-DD"),
    to_date: Optional[date] = Query(None, description="End date YYYY-MM-DD"),
    category: Optional[str] = Query(None, description="Category filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    service = AnalyticsService(db)
    return service.get_transactions(
        user_id=1,
        from_date=from_date,
        to_date=to_date,
        category=category,
        page=page,
        page_size=page_size,
    )


@router.get("/summary", response_model=TransactionSummaryResponse)
def get_transaction_summary(
    from_date: Optional[date] = Query(None, description="Start date YYYY-MM-DD"),
    to_date: Optional[date] = Query(None, description="End date YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    service = AnalyticsService(db)
    return service.get_transaction_summary(
        user_id=1,
        from_date=from_date,
        to_date=to_date,
    )
