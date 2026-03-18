import base64
import io
import importlib
import json
import logging

import httpx
from PIL import Image

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_vision_client = None


def _obter_vision_client_env_json():
    global _vision_client

    if _vision_client is not None:
        return _vision_client

    try:
        from google.cloud import vision
        service_account_mod = importlib.import_module("google.oauth2.service_account")
    except Exception as error:
        logger.warning("google-cloud-vision não disponível: %s", str(error))
        return None

    cred_json = (settings.GOOGLE_VISION_SERVICE_ACCOUNT_JSON or "").strip()
    if not cred_json:
        return None

    try:
        info = json.loads(cred_json)
        credenciais = service_account_mod.Credentials.from_service_account_info(info)
        _vision_client = vision.ImageAnnotatorClient(credentials=credenciais)
        logger.info("Google Vision inicializado com JSON de credencial no env")
        return _vision_client
    except Exception as error:
        logger.warning("Falha ao inicializar Google Vision com JSON do env: %s", str(error))

    return None


async def _ler_texto_google_vision_por_api_key(imagem_bytes: bytes) -> str:
    if not settings.GOOGLE_VISION_API_KEY:
        return ""

    endpoint = f"https://vision.googleapis.com/v1/images:annotate?key={settings.GOOGLE_VISION_API_KEY}"
    payload = {
        "requests": [
            {
                "image": {"content": base64.b64encode(imagem_bytes).decode("utf-8")},
                "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],
                "imageContext": {"languageHints": ["pt", "en"]},
            }
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as error:
        body = error.response.text if error.response is not None else ""
        logger.warning("Erro Google Vision via API key (status=%s): %s", error.response.status_code, body)
        return ""
    except httpx.HTTPError as error:
        logger.warning("Erro de rede Google Vision via API key: %s", str(error))
        return ""

    responses = data.get("responses", [])
    if not responses:
        return ""

    item = responses[0]
    if item.get("error", {}).get("message"):
        logger.warning("Erro retornado pelo Google Vision (API key): %s", item["error"]["message"])
        return ""

    full = item.get("fullTextAnnotation", {}).get("text", "").strip()
    if full:
        return full.replace("\n", " ").strip()

    annotations = item.get("textAnnotations", [])
    if annotations:
        return annotations[0].get("description", "").replace("\n", " ").strip()

    return ""


def _ler_texto_google_vision_env_json(imagem_bytes: bytes) -> str:
    client = _obter_vision_client_env_json()
    if client is None:
        return ""

    try:
        from google.cloud import vision

        image = vision.Image(content=imagem_bytes)
        response = client.document_text_detection(image=image)

        if response.error.message:
            logger.warning("Erro no Google Vision (env json): %s", response.error.message)
            return ""

        if response.full_text_annotation and response.full_text_annotation.text:
            return response.full_text_annotation.text.replace("\n", " ").strip()

        if response.text_annotations:
            return response.text_annotations[0].description.replace("\n", " ").strip()

        return ""
    except Exception as error:
        logger.warning("Erro no Google Vision OCR (env json): %s", str(error))
        return ""


async def extrair_textos_segmentados(imagem_bytes: bytes, bboxes: list[dict]) -> list[str]:
    if not imagem_bytes or not bboxes:
        return []

    try:
        imagem = Image.open(io.BytesIO(imagem_bytes)).convert("RGB")
    except Exception:
        return []

    width, height = imagem.size
    textos = []

    for box in bboxes:
        try:
            x1 = max(0, min(width, int(float(box.get("x1", 0)))))
            y1 = max(0, min(height, int(float(box.get("y1", 0)))))
            x2 = max(0, min(width, int(float(box.get("x2", 0)))))
            y2 = max(0, min(height, int(float(box.get("y2", 0)))))
        except (TypeError, ValueError):
            continue

        if x2 <= x1 or y2 <= y1:
            continue

        recorte = imagem.crop((x1, y1, x2, y2))
        buffer = io.BytesIO()
        recorte.save(buffer, format="JPEG", quality=95)

        recorte_bytes = buffer.getvalue()

        texto = await _ler_texto_google_vision_por_api_key(recorte_bytes)
        if not texto:
            texto = _ler_texto_google_vision_env_json(recorte_bytes)

        if texto:
            textos.append(texto)

    vistos = set()
    unicos = []
    for texto in textos:
        chave = texto.lower().strip()
        if not chave or chave in vistos:
            continue
        vistos.add(chave)
        unicos.append(texto)

    return unicos