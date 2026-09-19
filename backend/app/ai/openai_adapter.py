from typing import Any, Dict

from openai import OpenAI

from app.core.config import settings


class AIUnavailableError(RuntimeError):
    """Raised when optional AI configuration is not available."""


class OpenAIAdapter:
    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise AIUnavailableError("AI Q&A is unavailable until OPENAI_API_KEY is configured.")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def answer(self, question: str, context: Dict[str, Any]) -> str:
        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            temperature=0.2,
            max_tokens=350,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are FinAge, a personal finance decision-support assistant. "
                        "Answer only from the supplied structured data. Never invent amounts, "
                        "dates, or transactions. If the data is insufficient, say so plainly. "
                        "You may explain spending, budgets, recurring obligations, and goals, "
                        "but never provide investment, stock, trading, or financial-product advice. "
                        "Keep the answer concise and practical."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Structured financial context:\n{context}\n\nQuestion: {question}",
                },
            ],
        )
        content = response.choices[0].message.content if response.choices else None
        if not content:
            raise RuntimeError("The AI provider returned an empty answer.")
        return content.strip()
