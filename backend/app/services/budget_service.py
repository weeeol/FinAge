from datetime import date
from typing import Optional
import calendar
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.budget import Budget
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.budget import BudgetCreate, BudgetStatus, BudgetStatusList

class BudgetService:
    def __init__(self, db: Session):
        self.db = db

    def create_budget(self, user_id: int, data: BudgetCreate) -> Budget:
        category = self.db.query(Category).filter(Category.name == data.category).first()
        if not category:
            category = Category(name=data.category, kind="expense")
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)

        existing = self.db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category_id == category.id,
            Budget.month == data.month
        ).first()
        if existing:
            exc = HTTPException(status_code=409, detail="Budget for this category and month already exists.")
            exc.code = "duplicate_budget"
            raise exc

        budget = Budget(
            user_id=user_id,
            category_id=category.id,
            month=data.month,
            limit_minor=data.limit_minor,
            currency=data.currency
        )
        self.db.add(budget)
        self.db.commit()
        self.db.refresh(budget)

        return budget

    def get_budget_status(self, user_id: int, month: Optional[str] = None) -> BudgetStatusList:
        query = self.db.query(Budget).filter(Budget.user_id == user_id)
        if month:
            query = query.filter(Budget.month == month)

        budgets = query.all()
        status_items = []

        for b in budgets:
            category_name = b.category.name if b.category else "Unknown"

            year_str, month_str = b.month.split("-")
            year = int(year_str)
            month_int = int(month_str)
            
            start_date = date(year, month_int, 1)
            end_date = date(year, month_int, calendar.monthrange(year, month_int)[1])

            spent_result = self.db.query(func.sum(Transaction.amount_minor)).filter(
                Transaction.user_id == user_id,
                Transaction.category_id == b.category_id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).scalar()

            # expenses are negative, so spent is positive for subtraction
            spent_minor = -spent_result if spent_result else 0
            
            remaining_minor = b.limit_minor - spent_minor

            percent_used = 0.0
            if b.limit_minor > 0:
                percent_used = spent_minor / b.limit_minor

            if percent_used <= 0.85:
                status = "on_track"
            elif percent_used <= 1.0:
                status = "warning"
            else:
                status = "exceeded"

            status_items.append(BudgetStatus(
                budget_id=b.id,
                category=category_name,
                limit_minor=b.limit_minor,
                spent_minor=spent_minor,
                remaining_minor=remaining_minor,
                percent_used=percent_used,
                status=status
            ))

        return BudgetStatusList(items=status_items)
