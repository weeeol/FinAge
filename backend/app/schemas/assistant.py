from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class AssistantQuestion(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    from_date: Optional[date] = Field(None, description="Start date in YYYY-MM-DD format")
    to_date: Optional[date] = Field(None, description="End date in YYYY-MM-DD format")


class AssistantSource(BaseModel):
    kind: str
    label: str
    amount_minor: Optional[int] = None


class AssistantAnswer(BaseModel):
    answer: str
    sources: List[AssistantSource] = Field(default_factory=list)
