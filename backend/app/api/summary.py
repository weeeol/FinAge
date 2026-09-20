from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.summary import MonthlySummaryResponse
from app.services.summary_service import SummaryService

router = APIRouter(prefix="/monthly-summary", tags=["summary"])

@router.get("", response_model=MonthlySummaryResponse)
def get_monthly_summary(month: str, db: Session = Depends(get_db)):
    service = SummaryService(db)
    summary = service.get_monthly_summary(user_id=1, month=month)
    return summary
