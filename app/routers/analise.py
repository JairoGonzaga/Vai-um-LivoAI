from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.core.database import get_db
from app.schemas.sessao import SessaoResultado
from app.services import analise_service
 
router = APIRouter()


def _assinatura_valida_imagem(imagem_bytes: bytes) -> bool:
    if len(imagem_bytes) < 12:
        return False

    jpeg = imagem_bytes[0:3] == b"\xff\xd8\xff"
    png = imagem_bytes[0:8] == b"\x89PNG\r\n\x1a\n"
    gif = imagem_bytes[0:6] in (b"GIF87a", b"GIF89a")
    webp = imagem_bytes[0:4] == b"RIFF" and imagem_bytes[8:12] == b"WEBP"
    return jpeg or png or gif or webp
 
 

@router.post("", response_model=SessaoResultado, status_code=201)
@router.post("/", response_model=SessaoResultado, status_code=201, include_in_schema=False)
async def analisar_estante(
    foto: UploadFile = File(..., description="Foto da estante"),
    db:   AsyncSession = Depends(get_db),
):
    if not foto.content_type or not foto.content_type.startswith("image/"):
        raise HTTPException(status_code=422, detail="Arquivo deve ser uma imagem")

    imagem_bytes = await foto.read()
    if not _assinatura_valida_imagem(imagem_bytes):
        raise HTTPException(status_code=422, detail="Arquivo de imagem inválido")

    await foto.seek(0)
 
    return await analise_service.processar(db, foto)