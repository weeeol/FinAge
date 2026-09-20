from fastapi import APIRouter

from app.api.upload import router as upload_router
from app.api.transactions import router as transactions_router
from app.api.analytics import router as analytics_router
from app.api.assistant import router as assistant_router
from app.api.budgets import router as budgets_router
from app.api.goals import router as goals_router
from app.api.summary import router as summary_router
from app.api.database import router as database_router

api_router = APIRouter(prefix="/api")
api_router.include_router(upload_router)
api_router.include_router(transactions_router)
api_router.include_router(analytics_router)
api_router.include_router(assistant_router)
api_router.include_router(budgets_router)
api_router.include_router(goals_router)
api_router.include_router(summary_router)
api_router.include_router(database_router)
