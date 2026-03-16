from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str

    SUPABASE_URL:         str
    SUPABASE_ANON_KEY:    str
    SUPABASE_SERVICE_KEY: str
    STORAGE_BUCKET:       str = "Pratileiras"

    HF_SPACE_URL: str
    HF_TOKEN:     str

    GOOGLE_BOOKS_API_KEY: str

    APP_ENV:    str  = "development"
    APP_NAME:   str  = "LivroAI"
    API_PREFIX: str  = "/api/v1"
    DEBUG:      bool = True
    PORT:       int  = 8000

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    YOLO_CONFIDENCE_THRESHOLD: float = 0.6

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()