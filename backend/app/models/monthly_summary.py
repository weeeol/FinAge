from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MonthlySummary(Base):
    __tablename__ = "monthly_summaries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    month: Mapped[str] = mapped_column(String(7), nullable=False)  # YYYY-MM
    income_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    expense_minor: Mapped[int] = mapped_column(Integer, nullable=False)  # positive total
    net_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_count: Mapped[int] = mapped_column(Integer, nullable=False)
    top_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    generated_insight: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="monthly_summaries")
    top_category: Mapped[Optional["Category"]] = relationship("Category")

    __table_args__ = (
        UniqueConstraint("user_id", "month", name="uq_monthly_summary_user_month"),
    )
