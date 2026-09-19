from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FinPilot"
    API_PREFIX: str = "/api"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./data/finpilot.db"

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    UPLOAD_MAX_SIZE_BYTES: int = 10 * 1024 * 1024  # 10MB limit
    ALLOWED_UPLOAD_EXTENSIONS: List[str] = [".csv", ".xlsx", ".pdf"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
