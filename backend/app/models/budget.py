from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    month: Mapped[str] = mapped_column(String(7), nullable=False)  # YYYY-MM
    limit_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="budgets")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="budgets")

    __table_args__ = (
        UniqueConstraint("user_id", "category_id", "month", name="uq_budget_user_category_month"),
    )
