from fastapi import APIRouter

from app.api.upload import router as upload_router
from app.api.transactions import router as transactions_router
from app.api.analytics import router as analytics_router

api_router = APIRouter(prefix="/api")
api_router.include_router(upload_router)
api_router.include_router(transactions_router)
api_router.include_router(analytics_router)

