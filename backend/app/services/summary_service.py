from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.summary import InsightItem, TopCategory
from app.services.budget_service import BudgetService

class SummaryService:
    def __init__(self, db: Session):
        self.db = db

    def get_monthly_summary(self, user_id: int, month: str) -> dict:
        # Month format YYYY-MM
        year_str, month_str = month.split("-")
        y = int(year_str)
        m = int(month_str)
        
        # Calculate start and end date for the month
        from datetime import date, timedelta
        start_date = date(y, m, 1)
        if m == 12:
            end_date = date(y + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(y, m + 1, 1) - timedelta(days=1)

        # Get all transactions for the month
        txns = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).all()

        income_minor = sum(t.amount_minor for t in txns if t.amount_minor > 0)
        expense_minor = sum(t.amount_minor for t in txns if t.amount_minor < 0)
        net_minor = income_minor + expense_minor

        # Calculate top categories
        cat_totals = {}
        for t in txns:
            if t.amount_minor < 0:
                cname = t.category.name if t.category else "Unknown"
                cat_totals[cname] = cat_totals.get(cname, 0) + abs(t.amount_minor)

        sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
        top_categories = [{"category": k, "amount_minor": v} for k, v in sorted_cats[:3]]

        insights = []

        # Rule 1: Budget warnings
        budget_service = BudgetService(self.db)
        budgets_status = budget_service.get_budget_status(user_id=user_id, month=month)
        for b in budgets_status.items:
            if b.status in ["warning", "exceeded"]:
                insights.append(InsightItem(
                    type="budget",
                    title=f"Budget {b.status.title()}: {b.category}",
                    description=f"You have used {int(b.percent_used * 100)}% of your {b.category} budget.",
                    severity="warning"
                ))

        # Rule 2: Large single transactions (> 30% of total outflow)
        if expense_minor < 0:
            threshold = abs(expense_minor) * 0.30
            for t in txns:
                if t.amount_minor < 0 and abs(t.amount_minor) > threshold:
                    insights.append(InsightItem(
                        type="anomaly",
                        title="Large Expense Detected",
                        description=f"{t.description} accounts for >30% of this month's expenses.",
                        severity="warning"
                    ))

        # Optional LLM logic could go here (wrapped in try/except)
        # Using deterministic for now as instructed (if AI absent, return deterministic).

        return {
            "month": month,
            "income_minor": income_minor,
            "expense_minor": abs(expense_minor),
            "net_minor": net_minor,
            "top_categories": top_categories,
            "insights": insights
        }
