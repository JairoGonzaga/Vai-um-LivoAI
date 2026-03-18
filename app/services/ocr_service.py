import io
import importlib
import logging
import os
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)

_CREDENTIALS_FILENAME = "hybrid-cabinet-485920-a4-e0569960d34e.json"
_BASE_DIR = Path(__file__).resolve().parents[2]

_GOOGLE_VISION_CREDENTIALS_CANDIDATES = [
    str(_BASE_DIR / "app" / "cred" / _CREDENTIALS_FILENAME),
    f"/app/app/cred/{_CREDENTIALS_FILENAME}",
    str(Path.cwd() / "app" / "cred" / _CREDENTIALS_FILENAME),
]

_vision_client = None


def _obter_vision_client():
    global _vision_client

    if _vision_client is not None:
        return _vision_client

    try:
        from google.cloud import vision
        service_account_mod = importlib.import_module("google.oauth2.service_account")
    except Exception as error:
        logger.warning("google-cloud-vision não disponível: %s", str(error))
        return None

    caminho_env = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
    caminhos_candidatos = [
        caminho_env,
        *_GOOGLE_VISION_CREDENTIALS_CANDIDATES,
    ]

    for caminho in caminhos_candidatos:
        if not caminho:
            continue
        if not os.path.exists(caminho):
            continue

        try:
            credenciais = service_account_mod.Credentials.from_service_account_file(caminho)
            _vision_client = vision.ImageAnnotatorClient(credentials=credenciais)
            logger.info("Google Vision inicializado com credencial: %s", caminho)
            return _vision_client
        except Exception as error:
            logger.warning("Falha ao inicializar Google Vision com %s: %s", caminho, str(error))

    try:
        from google.cloud import vision
        _vision_client = vision.ImageAnnotatorClient()
        logger.info("Google Vision inicializado via GOOGLE_APPLICATION_CREDENTIALS/default credentials")
        return _vision_client
    except Exception as error:
        logger.warning("Não foi possível inicializar Google Vision: %s", str(error))
        return None


def ler_texto_google_vision(imagem_bytes: bytes) -> str:
    """Extrai texto de imagem usando Google Vision API (cliente oficial)."""
    client = _obter_vision_client()
    if client is None:
        return ""

    try:
        from google.cloud import vision

        image = vision.Image(content=imagem_bytes)
        response = client.document_text_detection(image=image)

        if response.error.message:
            logger.warning("Erro no Google Vision: %s", response.error.message)
            return ""

        if response.full_text_annotation and response.full_text_annotation.text:
            return response.full_text_annotation.text.replace("\n", " ").strip()

        if response.text_annotations:
            return response.text_annotations[0].description.replace("\n", " ").strip()

        return ""
    except Exception as error:
        logger.warning("Erro no Google Vision OCR: %s", str(error))
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

        texto = ler_texto_google_vision(buffer.getvalue())
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