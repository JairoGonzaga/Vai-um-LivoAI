from fastapi import FastAPI, Request

from app.routers import analise, livro, sessoes
from app.services import yolo_service
from app.core.config import get_settings
from app.core.database import engine
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import time
from uuid import uuid4

settings = get_settings()
logger = logging.getLogger("livroai.api")

if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


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
    allow_origin_regex=settings.ALLOWED_ORIGIN_REGEX or None,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("x-client-request-id") or str(uuid4())
    method = request.method
    path = request.url.path
    start = time.perf_counter()

    logger.info("request.started id=%s method=%s path=%s", request_id, method, path)

    try:
        response = await call_next(request)
    except Exception:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        logger.exception(
            "request.failed id=%s method=%s path=%s duration_ms=%s",
            request_id,
            method,
            path,
            elapsed_ms,
        )
        raise

    elapsed_ms = int((time.perf_counter() - start) * 1000)
    response.headers["x-request-id"] = request_id
    logger.info(
        "request.finished id=%s method=%s path=%s status=%s duration_ms=%s",
        request_id,
        method,
        path,
        response.status_code,
        elapsed_ms,
    )
    return response

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