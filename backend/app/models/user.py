from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True, unique=True, index=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="user", cascade="all, delete-orphan"
    )
    recurring_payments: Mapped[List["RecurringPayment"]] = relationship(
        "RecurringPayment", back_populates="user", cascade="all, delete-orphan"
    )
    budgets: Mapped[List["Budget"]] = relationship(
        "Budget", back_populates="user", cascade="all, delete-orphan"
    )
    goals: Mapped[List["FinancialGoal"]] = relationship(
        "FinancialGoal", back_populates="user", cascade="all, delete-orphan"
    )
    monthly_summaries: Mapped[List["MonthlySummary"]] = relationship(
        "MonthlySummary", back_populates="user", cascade="all, delete-orphan"
    )
