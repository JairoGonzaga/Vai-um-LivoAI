"""
Service responsavel pela lógica de negócios relacionada ao carregamento
e processamento de imagens usando o modelo YOLO, incluindo integração
com a API do YOLO e operações de banco de dados.

"""
import io
from ultralytics import YOLO
from PIL import Image
from app.core.config import get_settings

settings = get_settings()

_modelo: YOLO | None = None
 
 
def carregar_modelo() -> YOLO:
    global _modelo
    if _modelo is None:
        _modelo = YOLO(settings.YOLO_MODEL_PATH)
    return _modelo

