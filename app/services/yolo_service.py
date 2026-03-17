import httpx
from fastapi import HTTPException

from app.core.config import get_settings

settings = get_settings()


async def detectar(imagem_bytes: bytes, content_type: str) -> dict:
     headers = {}
     if settings.HF_TOKEN:
         headers["Authorization"] = f"Bearer {settings.HF_TOKEN}"

     async with httpx.AsyncClient() as client:
         try:
             resposta = await client.post(
                 f"{settings.HF_SPACE_URL.rstrip('/')}/detectar",
                 files={"imagem": ("foto.jpg", imagem_bytes, content_type)},
                 headers=headers,
                 timeout=60,
             )
             resposta.raise_for_status()
             return resposta.json()
         except httpx.TimeoutException:
             raise HTTPException(status_code=504, detail="Timeout na detecção")
         except httpx.HTTPStatusError as e:
             raise HTTPException(status_code=502, detail=f"Erro no serviço de detecção: {e.response.status_code}")
         except httpx.HTTPError:
             raise HTTPException(status_code=502, detail="Serviço de detecção indisponível")

    