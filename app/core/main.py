from fastapi import FastAPI

from app.routers import analise, livro, sessoes
from app.services import yolo_service
from app.core.config import get_settings
from app.core.database import engine
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield

    await engine.dispose()
    print("Database cleanup completed")

app = FastAPI(
    title=get_settings().APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
    docs_url = "/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.router.redirect_slashes = False

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.allowed_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(livro.router,  prefix=f"{settings.API_PREFIX}/livros",  tags=["Livros"])
app.include_router(analise.router, prefix=f"{settings.API_PREFIX}/analise", tags=["Analise"])
app.include_router(sessoes.router, prefix=f"{settings.API_PREFIX}/sessoes", tags=["Sessoes"])

@app.get("/", tags=["Root"])
async def root():
    return {
        "service": settings.APP_NAME,
        "status": "ok",
        "health": "/health",
        "api_prefix": settings.API_PREFIX,
    }

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "env": settings.APP_ENV}

@app.get(f"{settings.API_PREFIX}/health", tags=["Health"])
async def health_api_prefix():
    return {"status": "ok", "env": settings.APP_ENV}