from datetime import date
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.ai.openai_adapter import AIUnavailableError, OpenAIAdapter
from app.schemas.assistant import AssistantAnswer, AssistantSource
from app.services.analytics_service import AnalyticsService
from app.services.recurring_service import RecurringService


class QAService:
    def __init__(self, db: Session):
        self.db = db
        self.analytics = AnalyticsService(db)

    def answer(
        self,
        question: str,
        user_id: int = 1,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> AssistantAnswer:
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("Question cannot be empty.")

        context, sources = self._build_context(user_id, from_date, to_date)
        answer = OpenAIAdapter().answer(normalized_question, context)
        return AssistantAnswer(answer=answer, sources=sources)

    def _build_context(
        self,
        user_id: int,
        from_date: Optional[date],
        to_date: Optional[date],
    ) -> Tuple[Dict[str, Any], List[AssistantSource]]:
        summary = self.analytics.get_transaction_summary(user_id, from_date, to_date)
        categories = self.analytics.get_category_analytics(user_id)
        recurring = RecurringService(self.db).detect_and_sync_recurring(user_id)
        transactions = self.analytics.get_transactions(
            user_id=user_id,
            from_date=from_date,
            to_date=to_date,
            page=1,
            page_size=20,
        )

        sources = [
            AssistantSource(kind="summary", label="Income", amount_minor=summary.income_minor),
            AssistantSource(kind="summary", label="Expenses", amount_minor=summary.expense_minor),
            AssistantSource(kind="summary", label="Net", amount_minor=summary.net_minor),
        ]
        sources.extend(
            AssistantSource(kind="category_total", label=item.category, amount_minor=item.amount_minor)
            for item in categories.items[:5]
        )

        context = {
            "period": {"from_date": from_date.isoformat() if from_date else None, "to_date": to_date.isoformat() if to_date else None},
            "currency": summary.currency,
            "summary": summary.model_dump(),
            "categories": [item.model_dump() for item in categories.items[:10]],
            "recurring": [item.model_dump() for item in recurring.items[:10]],
            "transactions": [item.model_dump() for item in transactions.items],
        }
        return context, sources
