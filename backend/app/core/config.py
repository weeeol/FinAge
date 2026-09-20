import json
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    PROJECT_NAME: str = "FinAge"
    API_PREFIX: str = "/api"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./data/finage.db"

    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-3.6-flash"

    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"

    @property
    def cors_origins(self) -> List[str]:
        value = self.CORS_ORIGINS.strip()
        if not value:
            return []

        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            parsed = [origin.strip() for origin in value.split(",")]

        if isinstance(parsed, str):
            parsed = [parsed]
        return [origin.strip() for origin in parsed if origin and origin.strip()]

    UPLOAD_MAX_SIZE_BYTES: int = 10 * 1024 * 1024  # 10MB limit
    ALLOWED_UPLOAD_EXTENSIONS: List[str] = [".csv", ".xlsx", ".pdf"]

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
