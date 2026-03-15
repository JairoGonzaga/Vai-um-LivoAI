import uuid
from fastapi import UploadFile, HTTPException
from supabase import create_client, Client
from app.core.config import get_settings

settings = get_settings()

def get_supabase() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

async def upload(file: UploadFile) -> str:
    extensao = file.filename.split(".")[-1].lower()
    if extensao not in ["jpg", "jpeg", "png", "webp"]:
        raise HTTPException(
            status_code=422, 
            detail="Formato de imagem não suportado. Use jpg, jpeg, png ou webp."
        )

    imagem_bytes = await file.read()
    nome_arquivo = f"{uuid.uuid4()}.{extensao}"
    supabase = get_supabase()   

    try:
        supabase.storage.from_(settings.STORAGE_BUCKET_FOTOS).upload(
            path=nome_arquivo,
            file=imagem_bytes,
            file_options={"content-type": file.content_type},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao fazer upload da imagem para o Supabase."
        )

    url = supabase.storage.from_(settings.STORAGE_BUCKET_FOTOS).get_public_url(nome_arquivo)

    return url