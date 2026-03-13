from uuid import UUID
 
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.core.database import get_db
from app.schemas.livro import LivroCreate, LivroResponse
from app.services import livro_service
 
router = APIRouter()

# Catalogo de livros
@router.get("/", response_model=list[LivroResponse])
async def listar_livros(
    page:   int        = Query(1,    ge=1,          description="Número da página"),
    limit:  int        = Query(20,   ge=1,  le=100, description="Itens por página"),
    genero: str | None = Query(None,                description="Filtrar por gênero"),
    autor:  str | None = Query(None,                description="Filtrar por autor"),
    q:      str | None = Query(None,                description="Busca por nome do livro"),
    db: AsyncSession = Depends(get_db),
):
    livros = await livro_service.listar_livros(db, page, limit, genero, autor, q)
    if not livros:
        raise HTTPException(
            status_code=404,
            detail="Nenhum livro encontrado com os filtros fornecidos."
        )
    return livros

# Pega um livro específico
@router.get("/{isbn}", response_model=LivroResponse)
async def pegar_livro(
    isbn: str,
    db: AsyncSession = Depends(get_db),
):
    livro = await livro_service.pegar_livro_por_isbn(db, isbn)
    if not livro:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado."
        )
    
    return livro


@router.post("/", response_model=LivroResponse, status_code=201)
async def criar_livro(
    data: LivroCreate,
    db:   AsyncSession = Depends(get_db),
):
    return await livro_service.get_or_fetch(db, data)