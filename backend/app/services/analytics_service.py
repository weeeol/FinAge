from typing import Optional, List, Dict
from datetime import date
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.transaction import (
    TransactionItem,
    TransactionListResponse,
    TransactionSummaryResponse,
)
from app.schemas.analytics import (
    MonthlyAnalyticsItem,
    MonthlyAnalyticsResponse,
    CategoryAnalyticsItem,
    CategoryAnalyticsResponse,
)


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_transactions(
        self,
        user_id: int = 1,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> TransactionListResponse:
        page = max(1, page)
        page_size = max(1, min(100, page_size))

        query = (
            select(Transaction, Category.name.label("category_name"))
            .outerjoin(Category, Transaction.category_id == Category.id)
            .filter(Transaction.user_id == user_id)
        )

        if from_date:
            query = query.filter(Transaction.transaction_date >= from_date)
        if to_date:
            query = query.filter(Transaction.transaction_date <= to_date)
        if category:
            query = query.filter(Category.name == category)

        # Count total matching rows
        count_query = select(func.count()).select_from(query.subquery())
        total_count = self.db.execute(count_query).scalar_one()

        # Paginated results ordered latest first
        paged_query = (
            query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        results = self.db.execute(paged_query).all()

        items: List[TransactionItem] = []
        for txn, cat_name in results:
            items.append(
                TransactionItem(
                    id=txn.id,
                    date=txn.transaction_date.isoformat(),
                    description=txn.description,
                    amount_minor=txn.amount_minor,
                    currency=txn.currency,
                    category=cat_name or "Other",
                )
            )

        return TransactionListResponse(
            items=items,
            page=page,
            page_size=page_size,
            total=total_count,
        )

    def get_transaction_summary(
        self,
        user_id: int = 1,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> TransactionSummaryResponse:
        query = select(Transaction).filter(Transaction.user_id == user_id)

        if from_date:
            query = query.filter(Transaction.transaction_date >= from_date)
        if to_date:
            query = query.filter(Transaction.transaction_date <= to_date)

        txns = self.db.execute(query).scalars().all()

        income_minor = 0
        expense_minor = 0

        for t in txns:
            if t.amount_minor > 0:
                income_minor += t.amount_minor
            elif t.amount_minor < 0:
                expense_minor += abs(t.amount_minor)

        net_minor = income_minor - expense_minor

        return TransactionSummaryResponse(
            income_minor=income_minor,
            expense_minor=expense_minor,
            net_minor=net_minor,
            transaction_count=len(txns),
            currency="INR",
        )

    def get_monthly_analytics(
        self,
        user_id: int = 1,
        months: int = 6,
    ) -> MonthlyAnalyticsResponse:
        months = max(1, min(60, months))

        txns = (
            self.db.execute(
                select(Transaction)
                .filter(Transaction.user_id == user_id)
                .order_by(Transaction.transaction_date.asc())
            )
            .scalars()
            .all()
        )

        month_map: Dict[str, Dict[str, int]] = defaultdict(lambda: {"income": 0, "expense": 0})

        for t in txns:
            month_key = t.transaction_date.strftime("%Y-%m")
            if t.amount_minor > 0:
                month_map[month_key]["income"] += t.amount_minor
            elif t.amount_minor < 0:
                month_map[month_key]["expense"] += abs(t.amount_minor)

        # Sort all present months chronologically
        sorted_keys = sorted(month_map.keys())
        if len(sorted_keys) > months:
            sorted_keys = sorted_keys[-months:]

        items: List[MonthlyAnalyticsItem] = []
        for m in sorted_keys:
            inc = month_map[m]["income"]
            exp = month_map[m]["expense"]
            items.append(
                MonthlyAnalyticsItem(
                    month=m,
                    income_minor=inc,
                    expense_minor=exp,
                    net_minor=inc - exp,
                )
            )

        return MonthlyAnalyticsResponse(items=items)

    def get_category_analytics(
        self,
        user_id: int = 1,
        month: Optional[str] = None,
    ) -> CategoryAnalyticsResponse:
        query = (
            select(Transaction, Category.name.label("category_name"))
            .outerjoin(Category, Transaction.category_id == Category.id)
            .filter(Transaction.user_id == user_id, Transaction.amount_minor < 0)
        )

        results = self.db.execute(query).all()

        cat_amounts: Dict[str, int] = defaultdict(int)
        cat_counts: Dict[str, int] = defaultdict(int)
        total_expense = 0

        for txn, cat_name in results:
            txn_month = txn.transaction_date.strftime("%Y-%m")
            if month and txn_month != month:
                continue

            name = cat_name or "Other"
            abs_amount = abs(txn.amount_minor)
            cat_amounts[name] += abs_amount
            cat_counts[name] += 1
            total_expense += abs_amount

        items: List[CategoryAnalyticsItem] = []
        # Sort by highest spending category first
        for cat in sorted(cat_amounts.keys(), key=lambda c: cat_amounts[c], reverse=True):
            amount = cat_amounts[cat]
            share = round(amount / total_expense, 4) if total_expense > 0 else 0.0
            items.append(
                CategoryAnalyticsItem(
                    category=cat,
                    amount_minor=amount,
                    transaction_count=cat_counts[cat],
                    share=share,
                )
            )

        return CategoryAnalyticsResponse(items=items)
