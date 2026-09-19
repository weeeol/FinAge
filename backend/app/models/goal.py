from datetime import date, datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FinancialGoal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    target_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    current_minor: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    target_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="goals")

    __table_args__ = (
        Index("ix_goals_user_target_date", "user_id", "target_date"),
    )
