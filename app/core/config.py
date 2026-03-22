from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import json


class Settings(BaseSettings):
    DATABASE_URL: str

    SUPABASE_URL:         str
    SUPABASE_ANON_KEY:    str
    SUPABASE_SERVICE_KEY: str
    STORAGE_BUCKET:       str = "Pratileiras"
    STORAGE_BUCKET_FOTOS: str = "Pratileiras"

    HF_SPACE_URL: str = ""
    HF_TOKEN:     str = ""

    ROBOFLOW_API_URL: str = "https://serverless.roboflow.com"
    ROBOFLOW_API_KEY: str = ""
    ROBOFLOW_WORKSPACE_NAME: str = ""
    ROBOFLOW_WORKFLOW_ID: str = ""
    ROBOFLOW_IMAGE_INPUT_KEY: str = "image"

    GOOGLE_BOOKS_API_KEY: str
    GOOGLE_VISION_CREDENTIALS: str = ""
    MISTRAL_API_KEY: str = ""

    APP_ENV:    str  = "development"
    APP_NAME:   str  = "LivroAI"
    API_PREFIX: str  = "/api/v1"
    DEBUG:      bool = False
    PORT:       int  = 8000

    ALLOWED_ORIGINS: str 
    ALLOWED_ORIGIN_REGEX: str 
    API_KEY: str = ""
    ENFORCE_API_KEY: bool = True
    SESSION_TOKEN_SECRET: str = ""

    YOLO_CONFIDENCE_THRESHOLD: float = 0.6

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        value = (self.ALLOWED_ORIGINS or "").strip()
        origins = []
        
        if not value:
            origins = []
        elif value.startswith("["):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    origins = [str(item).strip() for item in parsed if str(item).strip()]
            except json.JSONDecodeError:
                origins = []
        else:
            origins = [item.strip() for item in value.split(",") if item.strip()]
        
        # Always allow localhost in dev
        if self.APP_ENV == "development" or self.DEBUG:
            origins.extend(["http://localhost:3000", "http://localhost:5173"])
        
        return origins


@lru_cache
def get_settings() -> Settings:
    return Settings()