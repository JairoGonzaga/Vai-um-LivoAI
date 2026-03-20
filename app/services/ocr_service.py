import base64
import io
import importlib
import json
import logging
import os

import httpx
from PIL import Image

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_vision_client = None
_vision_client_init_attempted = False
_GOOGLE_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


def _obter_vision_client_env_json():
    global _vision_client
    global _vision_client_init_attempted

    if _vision_client is not None:
        return _vision_client

    if _vision_client_init_attempted:
        return None

    _vision_client_init_attempted = True

    try:
        from google.cloud import vision
        service_account_mod = importlib.import_module("google.oauth2.service_account")
    except Exception as error:
        logger.warning("google-cloud-vision não disponível: %s", str(error))
        return None

    cred_json = (settings.GOOGLE_VISION_CREDENTIALS or "").strip()

    if not cred_json:
        logger.warning("GOOGLE_VISION_CREDENTIALS vazia. Vision OCR desativado.")
        return None

    logger.info(
        "Tentando inicializar Google Vision com JSON (tamanho: %d bytes, começa com: %s, termina com: %s)",
        len(cred_json),
        cred_json[:30] if len(cred_json) > 30 else cred_json,
        cred_json[-10:] if len(cred_json) > 10 else cred_json,
    )

    try:
        info = json.loads(cred_json)
        credenciais = service_account_mod.Credentials.from_service_account_info(
            info,
            scopes=_GOOGLE_SCOPES,
        )
        _vision_client = vision.ImageAnnotatorClient(credentials=credenciais)
        logger.info("Google Vision inicializado com JSON de credencial no env")
        return _vision_client
    except Exception as error:
        logger.warning("Falha ao inicializar Google Vision com JSON do env: %s", str(error))

    return None


async def _ler_texto_google_vision_por_api_key(imagem_bytes: bytes) -> str:
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
        logger.info("ocr.extrair_textos_segmentados entrada vazia")
        return []

    try:
        imagem = Image.open(io.BytesIO(imagem_bytes)).convert("RGB")
    except Exception as e:
        logger.error("ocr.extrair_textos_segmentados falha ao abrir imagem: %s", str(e))
        return []

    width, height = imagem.size
    logger.info("ocr.extrair_textos_segmentados dimensões imagem: %sx%s", width, height)
    textos = []

    for i, box in enumerate(bboxes):
        try:
            x1 = max(0, min(width, int(float(box.get("x1", 0)))))
            y1 = max(0, min(height, int(float(box.get("y1", 0)))))
            x2 = max(0, min(width, int(float(box.get("x2", 0)))))
            y2 = max(0, min(height, int(float(box.get("y2", 0)))))
        except (TypeError, ValueError) as e:
            logger.warning("ocr.extrair_textos_segmentados bbox %s - erro ao extrair coordenadas: %s", i, str(e))
            continue

        if x2 <= x1 or y2 <= y1:
            logger.warning("ocr.extrair_textos_segmentados bbox %s - coordenadas inválidas: (%s,%s)-(%s,%s)", i, x1, y1, x2, y2)
            continue

        recorte = imagem.crop((x1, y1, x2, y2))
        buffer = io.BytesIO()
        recorte.save(buffer, format="JPEG", quality=95)

        recorte_bytes = buffer.getvalue()

        texto = await _ler_texto_google_vision_por_api_key(recorte_bytes)
        if not texto:
            texto = _ler_texto_google_vision_env_json(recorte_bytes)

        logger.info("ocr.extrair_textos_segmentados bbox %s - texto extraído: '%s'", i, texto[:100] if texto else "(vazio)")
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

    logger.info("ocr.extrair_textos_segmentados deduplicação: %s textos → %s únicos", len(textos), len(unicos))
    return unicos