from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.db.init_db import init_db
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed data on startup
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FinAge - Personal Finance Decision-Support Agent API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_error",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": getattr(exc, "code", "http_error"),
                "message": str(exc.detail),
                "details": getattr(exc, "details", {}),
            }
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Log securely without leaking stack trace to client
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_error",
                "message": "An internal server error occurred",
                "details": {},
            }
        },
    )


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
