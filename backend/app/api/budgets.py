from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.budget import BudgetCreate, BudgetResponse
from app.services.budget_service import BudgetService

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.post("", response_model=BudgetResponse, status_code=201)
def create_budget(data: BudgetCreate, db: Session = Depends(get_db)):
    service = BudgetService(db)
    budget = service.create_budget(user_id=1, data=data)
    
    return BudgetResponse(
        id=budget.id,
        category=budget.category.name if budget.category else "Unknown",
        month=budget.month,
        limit_minor=budget.limit_minor,
        currency=budget.currency,
        created_at=budget.created_at
    )

@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    service = BudgetService(db)
    deleted_id = service.delete_budget(user_id=1, budget_id=budget_id)
    return {"deleted": True, "id": deleted_id}
