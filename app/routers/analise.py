from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.core.database import get_db
from app.schemas.sessao import SessaoResultado
from app.services import analise_service
 
router = APIRouter()
 
 

@router.post("/", response_model=SessaoResultado, status_code=201)
async def analisar_estante(
    foto: UploadFile = File(..., description="Foto da estante"),
    db:   AsyncSession = Depends(get_db),
):
    if not foto.content_type.startswith("image/"):
        raise HTTPException(status_code=422, detail="Arquivo deve ser uma imagem")
 
    return await analise_service.processar(db, foto)