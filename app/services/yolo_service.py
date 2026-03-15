# app/services/yolo_service.py

import io
from ultralytics import YOLO
from PIL import Image
from huggingface_hub import hf_hub_download

from app.core.config import get_settings

settings = get_settings()

_modelo: YOLO | None = None


def inicializar():
    global _modelo

    caminho = hf_hub_download(
        repo_id=settings.HF_MODEL_REPO_ID,
        filename=settings.HF_MODEL_FILENAME,
        token=settings.HF_TOKEN,
    )

    _modelo = YOLO(caminho)


def carregar_modelo() -> YOLO:
    if _modelo is None:
        raise RuntimeError("Modelo YOLO não foi inicializado — verifique o lifespan do main.py")
    return _modelo


async def detectar(imagem_bytes: bytes) -> dict:
    imagem = Image.open(io.BytesIO(imagem_bytes))
    modelo = carregar_modelo()

    resultados = modelo(imagem, conf=settings.YOLO_CONFIDENCE_THRESHOLD)

    bboxes           = []
    nomes_detectados = []

    for resultado in resultados:
        for box in resultado.boxes:
            confianca = float(box.conf[0])
            classe_id = int(box.cls[0])
            nome      = resultado.names[classe_id]

            x1, y1, x2, y2 = [float(c) for c in box.xyxy[0]]

            bboxes.append({
                "x1":        x1,
                "y1":        y1,
                "x2":        x2,
                "y2":        y2,
                "confianca": confianca,
                "nome":      nome,
            })

            if nome not in nomes_detectados:
                nomes_detectados.append(nome)

    return {
        "bboxes":           bboxes,
        "nomes_detectados": nomes_detectados,
    }