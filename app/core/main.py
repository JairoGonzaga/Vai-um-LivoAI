from fastapi import FastAPI
from .config import get_settings
from .database import engine
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    print("Database opened")

    yield

    await engine.dispose()
    print("Database closed")

app = FastAPI(
    title=get_settings().LIVROAI,
    version="1.0.0",
    lifespan=lifespan,
    docs_url = "/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.add.middleware(
    CORSMiddleware,
    allow_origins = settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

#rotas entram aqui

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "env": settings.APP_ENV}