from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str

    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str


    APP_ENV: str = 'development'
    APP_NAME: str = 'LivroAI'
    API_PREFIX: str = '/api/V1'
    DEBUG: bool = True

    ALLOWED_HOSTS: list[str] = [
        "http://localhost:5173",   
        "http://localhost:3000",]
    
    STORAGE_BUCKET: str = 'Pratileiras'

    YOLO_MODEL_PATH: str = '../models/yolov8m-seg.pt'
    YOLO_TRESHOLD: float = 0.6

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

@lru_cache()
def get_settings():
    return Settings()