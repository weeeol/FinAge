import os
import logging
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine, SessionLocal
import app.models  # Ensure all models are loaded into Base.metadata
from app.models.user import User
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.recurring_payment import RecurringPayment
from app.models.budget import Budget
from app.models.goal import FinancialGoal
from app.models.monthly_summary import MonthlySummary

logger = logging.getLogger("finage.db")

DEFAULT_CATEGORIES = [
    # Income
    {"name": "Salary", "kind": "income"},
    {"name": "Investment Income", "kind": "income"},
    {"name": "Freelance", "kind": "income"},
    {"name": "Refund", "kind": "income"},
    # Expense
    {"name": "Groceries", "kind": "expense"},
    {"name": "Dining & Food", "kind": "expense"},
    {"name": "Housing & Rent", "kind": "expense"},
    {"name": "Utilities", "kind": "expense"},
    {"name": "Transport", "kind": "expense"},
    {"name": "Shopping", "kind": "expense"},
    {"name": "Entertainment", "kind": "expense"},
    {"name": "Subscription", "kind": "expense"},
    {"name": "Healthcare", "kind": "expense"},
    {"name": "Travel", "kind": "expense"},
    {"name": "Personal Care", "kind": "expense"},
    {"name": "Education", "kind": "expense"},
    {"name": "Financial Services", "kind": "expense"},
    # Transfer & Other
    {"name": "Transfer", "kind": "transfer"},
    {"name": "Other", "kind": "other"},
]


def init_db(db_session: Session = None) -> None:
    """
    Ensure directories exist, create tables, and seed default user and categories.
    Can be passed an existing session (useful for unit tests) or use default engine.
    """
    # If SQLite file path, ensure directory exists
    if settings.DATABASE_URL.startswith("sqlite:///"):
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    Base.metadata.create_all(bind=engine)

    session = db_session if db_session is not None else SessionLocal()
    try:
        # Seed default user if not present
        demo_user = session.execute(select(User).filter_by(id=1)).scalar_one_or_none()
        if not demo_user:
            demo_user = User(
                id=1,
                name="Demo User",
                email="demo@finage.local",
                currency="USD",
            )
            session.add(demo_user)
            session.commit()
            logger.info("Seeded default demo user (id=1)")

        # Seed default categories if not present
        existing_categories = {c.name: c for c in session.execute(select(Category)).scalars().all()}
        added_count = 0
        for cat_data in DEFAULT_CATEGORIES:
            if cat_data["name"] not in existing_categories:
                category = Category(
                    name=cat_data["name"],
                    kind=cat_data["kind"],
                )
                session.add(category)
                added_count += 1

        if added_count > 0:
            session.commit()
            logger.info(f"Seeded {added_count} standard categories")

    finally:
        if db_session is None:
            session.close()


def reset_demo_data(db_session: Session) -> None:
    """Remove demo-owned financial data while preserving the user and categories."""
    for model in (MonthlySummary, RecurringPayment, Budget, FinancialGoal, Transaction):
        db_session.query(model).delete(synchronize_session=False)
    db_session.commit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
    print("Database initialized successfully.")
