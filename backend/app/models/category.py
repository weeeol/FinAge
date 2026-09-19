from datetime import datetime, timezone
from typing import List
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    kind: Mapped[str] = mapped_column(String, nullable=False, default="expense")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )
    recurring_payments: Mapped[List["RecurringPayment"]] = relationship(
        "RecurringPayment", back_populates="category"
    )
    budgets: Mapped[List["Budget"]] = relationship(
        "Budget", back_populates="category"
    )
