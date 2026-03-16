"""
Service Responsavel pela lógica de negócios relacionada aos livros,
 incluindo busca, integração com a API do Google Books e operações de banco de dados.
"""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
from app.core.config import get_settings
from app.models.livro import Livro
from app.schemas.livro import LivroCreate

settings = get_settings()

async def buscar_isbn(db: AsyncSession, isbn: str) -> Livro | None:
    result = await db.execute(select(Livro).where(Livro.isbn == isbn))
    return result.scalar_one_or_none()

async def buscar_nome(db: AsyncSession, nome: str) -> Livro | None:
    result = await db.execute(select(Livro).where(Livro.nome.ilike(f"%{nome}%")))
    return result.scalar_one_or_none()

async def buscar_no_google_books(nome: str) -> dict | None:
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
                return None
 
            item = dados["items"][0]["volumeInfo"]
 
            isbn = None
            for identificador in item.get("industryIdentifiers", []):
                if identificador["type"] == "ISBN_13":
                    isbn = identificador["identifier"]
                    break
                if identificador["type"] == "ISBN_10":
                    isbn = identificador["identifier"]
 
            return {
                "nome":           item.get("title"),
                "autor":          item.get("authors", [None])[0],
                "genero":         item.get("categories", [None])[0],
                "isbn":           isbn,
                "link":           item.get("infoLink"),
                "capa_url":       item.get("imageLinks", {}).get("thumbnail"),
                "sinopse":        item.get("description"),
                "ano_publicacao": int(item["publishedDate"][:4]) if item.get("publishedDate") else None,
                "editora":        item.get("publisher"),
            }
 
        except (httpx.HTTPError, KeyError, ValueError):
            return None
        
async def salvar_livro(db: AsyncSession, livro_data: LivroCreate) -> Livro:
    novo_livro = Livro(**livro_data.model_dump())
    db.add(novo_livro)
    await db.flush()
    return novo_livro

async def get_or_fetch(db: AsyncSession, nome: str | LivroCreate) -> Livro | None:
    if isinstance(nome, LivroCreate):
        nome = nome.nome

    livro = await buscar_nome(db, nome)
    if livro:
        return livro
    
    dados_google = await buscar_no_google_books(nome)
    if not dados_google:
        return None
    
    if dados_google.get("isbn"):
        livro = await buscar_isbn(db, dados_google["isbn"])
        if livro:
            return livro
    
    livro_data = LivroCreate(**dados_google)
    return await salvar_livro(db, livro_data)   

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