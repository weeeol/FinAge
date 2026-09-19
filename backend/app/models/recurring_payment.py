from datetime import date, datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Float, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class RecurringPayment(Base):
    __tablename__ = "recurring_payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    merchant_name: Mapped[str] = mapped_column(String, nullable=False)
    typical_amount_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    frequency: Mapped[str] = mapped_column(String, nullable=False, default="monthly")  # weekly|monthly|annual|unknown
    next_expected_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    last_seen_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="recurring_payments")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="recurring_payments")

    __table_args__ = (
        Index("ix_recurring_payments_user_next_date", "user_id", "next_expected_date"),
    )
