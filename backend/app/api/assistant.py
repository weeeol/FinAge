from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.ai.gemini_adapter import AIUnavailableError
from app.db.session import get_db
from app.schemas.assistant import AssistantAnswer, AssistantQuestion
from app.services.qa_service import QAService

router = APIRouter(tags=["Assistant"])


@router.post("/ask", response_model=AssistantAnswer)
def ask_finage(question: AssistantQuestion, db: Session = Depends(get_db)):
    try:
        return QAService(db).answer(
            question=question.question,
            user_id=1,
            from_date=question.from_date,
            to_date=question.to_date,
        )
    except AIUnavailableError as exc:
        return JSONResponse(
            status_code=503,
            content={
                "error": {
                    "code": "ai_unavailable",
                    "message": str(exc),
                    "details": {},
                }
            },
        )
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": "empty_question",
                    "message": str(exc),
                    "details": {},
                }
            },
        )