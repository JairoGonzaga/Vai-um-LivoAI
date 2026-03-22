"""
Service Responsavel pela lógica de negócios relacionada aos livros,
 incluindo busca, integração com a API do Google Books e operações de banco de dados.
"""
import uuid
import logging
import time

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
from app.core.config import get_settings
from app.models.livro import Livro
from app.schemas.livro import LivroCreate

settings = get_settings()
logger = logging.getLogger(__name__)

_GOOGLE_BOOKS_CACHE_TTL_SECONDS = 900
_google_books_cache: dict[str, tuple[float, dict | None]] = {}
_CACHE_MISS = object()
_DADOS_GOOGLE_NAO_INFORMADOS = object()


def _cache_google_books_get(chave: str) -> dict | None | object:
    item = _google_books_cache.get(chave)
    if not item:
        return _CACHE_MISS

    salvo_em, valor = item
    if time.time() - salvo_em > _GOOGLE_BOOKS_CACHE_TTL_SECONDS:
        _google_books_cache.pop(chave, None)
        return _CACHE_MISS

    return valor


def _cache_google_books_set(chave: str, valor: dict | None) -> None:
    _google_books_cache[chave] = (time.time(), valor)

async def buscar_isbn(db: AsyncSession, isbn: str) -> Livro | None:
    result = await db.execute(select(Livro).where(Livro.isbn == isbn))
    return result.scalar_one_or_none()

async def buscar_nome(db: AsyncSession, nome: str) -> Livro | None:
    result = await db.execute(select(Livro).where(Livro.nome.ilike(f"%{nome}%")))
    return result.scalar_one_or_none()

async def buscar_no_google_books(nome: str) -> dict | None:
    chave_cache = nome.strip().lower()
    if chave_cache:
        valor_cache = _cache_google_books_get(chave_cache)
        if valor_cache is not _CACHE_MISS:
            return valor_cache

    async with httpx.AsyncClient() as client:
        try:
            resposta = await client.get(
                "https://www.googleapis.com/books/v1/volumes",
                params={"q": nome, "key": settings.GOOGLE_BOOKS_API_KEY},
                timeout=10,
            )
            resposta.raise_for_status()
            dados = resposta.json()
 
            if not dados.get("items"):
                if chave_cache:
                    _cache_google_books_set(chave_cache, None)
                return None
 
            item = dados["items"][0]["volumeInfo"]

            nome_livro = item.get("title")
            if not nome_livro:
                if chave_cache:
                    _cache_google_books_set(chave_cache, None)
                return None

            autor_livro = item.get("authors", [None])[0] or "Autor desconhecido"
 
            isbn = None
            for identificador in item.get("industryIdentifiers", []):
                if identificador["type"] == "ISBN_13":
                    isbn = identificador["identifier"]
                    break
                if identificador["type"] == "ISBN_10":
                    isbn = identificador["identifier"]
 
            resultado = {
                "nome":           nome_livro,
                "autor":          autor_livro,
                "genero":         item.get("categories", [None])[0],
                "isbn":           isbn,
                "link":           item.get("infoLink"),
                "capa_url":       item.get("imageLinks", {}).get("thumbnail"),
                "sinopse":        item.get("description"),
                "ano_publicacao": int(item["publishedDate"][:4]) if item.get("publishedDate") else None,
                "editora":        item.get("publisher"),
            }

            if chave_cache:
                _cache_google_books_set(chave_cache, resultado)

            return resultado
 
        except (httpx.HTTPError, KeyError, ValueError):
            if chave_cache:
                _cache_google_books_set(chave_cache, None)
            return None
        
async def salvar_livro(db: AsyncSession, livro_data: LivroCreate) -> Livro:
    payload = livro_data.model_dump()
    if not payload.get("autor"):
        payload["autor"] = "Autor desconhecido"

    novo_livro = Livro(**payload)
    db.add(novo_livro)
    await db.flush()
    return novo_livro

async def get_or_fetch(
    db: AsyncSession,
    nome: str | LivroCreate,
    dados_google_precarregado: dict | None | object = _DADOS_GOOGLE_NAO_INFORMADOS,
) -> Livro | None:
    if isinstance(nome, LivroCreate):
        nome = nome.nome

    if not nome or not str(nome).strip():
        return None

    nome = str(nome).strip()

    livro = await buscar_nome(db, nome)
    if livro:
        return livro
    
    if dados_google_precarregado is _DADOS_GOOGLE_NAO_INFORMADOS:
        dados_google = await buscar_no_google_books(nome)
    else:
        dados_google = dados_google_precarregado

    if not dados_google:
        return None
    
    if dados_google.get("isbn"):
        livro = await buscar_isbn(db, dados_google["isbn"])
        if livro:
            return livro
    
    try:
        livro_data = LivroCreate(**dados_google)
        return await salvar_livro(db, livro_data)
    except Exception as error:
        logger.warning("Ignorando nome sem dados válidos para salvar no Google Books: %s (%s)", nome, str(error))
        return None

async def listar( # definimos limites e parametros de busca
    db:     AsyncSession,
    page:   int = 1,
    limit:  int = 20,
    genero: str | None = None,
    autor:  str | None = None,
    q:      str | None = None,
) -> list[Livro]:
    querry = select(Livro)

    if genero:
        querry = querry.where(Livro.genero.ilike(f"%{genero}%"))
    if autor:
        querry = querry.where(Livro.autor.ilike(f"%{autor}%"))
    if q:
        querry = querry.where(Livro.nome.ilike(f"%{q}%"))
    querry = querry.offset((page - 1) * limit).limit(limit)
    result = await db.execute(querry)
    return result.scalars().all()

async def obter_por_idorisbn(db: AsyncSession, isbn: str) -> Livro | None:
    livro = await buscar_isbn(db, isbn)
    if livro:
        return livro
    try:
        uuid_val = uuid.UUID(isbn)
        result = await db.execute(select(Livro).where(Livro.id == uuid_val))
        return result.scalar_one_or_none()
    except ValueError:
        return None