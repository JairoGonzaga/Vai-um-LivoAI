import httpx
from fastapi import HTTPException

from app.core.config import get_settings

settings = get_settings()


def _validar_config_roboflow() -> None:
     faltantes = []
     if not settings.ROBOFLOW_API_KEY:
         faltantes.append("ROBOFLOW_API_KEY")
     if not settings.ROBOFLOW_WORKSPACE_NAME:
         faltantes.append("ROBOFLOW_WORKSPACE_NAME")
     if not settings.ROBOFLOW_WORKFLOW_ID:
         faltantes.append("ROBOFLOW_WORKFLOW_ID")

     if faltantes:
         raise HTTPException(
             status_code=500,
             detail=f"Configuração Roboflow incompleta: {', '.join(faltantes)}",
         )


def _extrair_predictions(payload: dict) -> list[dict]:
     if not isinstance(payload, dict):
         return []

     for valor in payload.values():
         if not isinstance(valor, dict):
             continue
         predictions = valor.get("predictions")
         if isinstance(predictions, list):
             return predictions

     return []


def _normalizar_bboxes(predictions: list[dict]) -> list[dict]:
     bboxes = []
     limiar = float(settings.YOLO_CONFIDENCE_THRESHOLD)

     for pred in predictions:
         if not isinstance(pred, dict):
             continue

         try:
             confianca = float(pred.get("confidence", 0))
             x = float(pred.get("x", 0))
             y = float(pred.get("y", 0))
             largura = float(pred.get("width", 0))
             altura = float(pred.get("height", 0))
         except (TypeError, ValueError):
             continue

         if confianca < limiar or largura <= 0 or altura <= 0:
             continue

         x1 = max(0, x - (largura / 2))
         y1 = max(0, y - (altura / 2))
         x2 = max(x1, x + (largura / 2))
         y2 = max(y1, y + (altura / 2))

         bboxes.append(
             {
                 "x1": int(round(x1)),
                 "y1": int(round(y1)),
                 "x2": int(round(x2)),
                 "y2": int(round(y2)),
                 "score": confianca,
                 "class_id": pred.get("class_id"),
                 "class_name": pred.get("class"),
                 "detection_id": pred.get("detection_id"),
             }
         )

     return bboxes


async def detectar(imagem_bytes: bytes, content_type: str) -> dict:
     _validar_config_roboflow()

     async with httpx.AsyncClient() as client:
         try:
             arquivo_nome = "foto.jpg"
             extensao = (content_type or "").split("/")[-1].lower()
             if extensao in {"png", "webp", "gif", "jpeg", "jpg"}:
                 arquivo_nome = f"foto.{extensao if extensao != 'jpeg' else 'jpg'}"

             resposta = await client.post(
                 f"{settings.ROBOFLOW_API_URL.rstrip('/')}/{settings.ROBOFLOW_WORKSPACE_NAME}/{settings.ROBOFLOW_WORKFLOW_ID}",
                 params={"api_key": settings.ROBOFLOW_API_KEY},
                 files={settings.ROBOFLOW_IMAGE_INPUT_KEY: (arquivo_nome, imagem_bytes, content_type or "image/jpeg")},
                 timeout=60,
             )
             resposta.raise_for_status()

             corpo = resposta.json()
             if isinstance(corpo, list) and corpo:
                 payload = corpo[0]
             elif isinstance(corpo, dict):
                 payload = corpo
             else:
                 payload = {}

             predictions = _extrair_predictions(payload)
             bboxes = _normalizar_bboxes(predictions)
             return {"bboxes": bboxes, "raw": corpo}
         except httpx.TimeoutException:
             raise HTTPException(status_code=504, detail="Timeout na detecção")
         except httpx.HTTPStatusError as e:
             raise HTTPException(status_code=502, detail=f"Erro no serviço de detecção: {e.response.status_code}")
         except httpx.HTTPError:
             raise HTTPException(status_code=502, detail="Serviço de detecção indisponível")

    