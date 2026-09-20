from typing import Any, Dict

from google import genai
from google.genai import types

from app.core.config import settings


class AIUnavailableError(RuntimeError):
    """Raised when optional AI configuration is not available."""


class GeminiAdapter:
    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise AIUnavailableError("AI Q&A is unavailable until GEMINI_API_KEY is configured.")
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def answer(self, question: str, context: Dict[str, Any]) -> str:
        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=f"Structured financial context:\n{context}\n\nQuestion: {question}",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are FinAge, a personal finance decision-support assistant. "
                    "Answer only from the supplied structured data. Never invent amounts, "
                    "dates, or transactions. If the data is insufficient, say so plainly. "
                    "You may explain spending, budgets, recurring obligations, and goals, "
                    "but never provide investment, stock, trading, or financial-product advice. "
                    "Keep the answer concise and practical."
                ),
                temperature=0.2,
                max_output_tokens=350,
            ),
        )
        content = response.text
        if not content:
            raise RuntimeError("The AI provider returned an empty answer.")
        return content.strip()