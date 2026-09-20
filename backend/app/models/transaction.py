from datetime import date, datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Boolean, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    amount_minor: Mapped[int] = mapped_column(Integer, nullable=False)  # positive income, negative expense
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")
    source_file: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    external_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_recurring_candidate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="transactions")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="transactions")

    __table_args__ = (
        Index("ix_transactions_user_date", "user_id", "transaction_date"),
        Index("ix_transactions_user_category", "user_id", "category_id"),
        Index("ix_transactions_user_description", "user_id", "description"),
    )
