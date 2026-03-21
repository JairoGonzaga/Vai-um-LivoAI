from datetime import datetime, timezone
from uuid import UUID

from jose import JWTError, ExpiredSignatureError, jwt

from app.core.config import get_settings

settings = get_settings()
ALGORITHM = "HS256"


def gerar_token_sessao(sessao_id: UUID, expira_em: datetime) -> str:
    segredo = (settings.SESSION_TOKEN_SECRET or "").strip()
    if not segredo:
        return ""

    expira_utc = expira_em.astimezone(timezone.utc)
    payload = {
        "sid": str(sessao_id),
        "exp": int(expira_utc.timestamp()),
    }
    return jwt.encode(payload, segredo, algorithm=ALGORITHM)


def extrair_token_sessao(
    authorization: str | None,
    x_session_token: str | None,
) -> str:
    if x_session_token and x_session_token.strip():
        return x_session_token.strip()

    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()

    return ""


def validar_token_sessao(token: str, sessao_id: UUID) -> bool:
    segredo = (settings.SESSION_TOKEN_SECRET or "").strip()
    if not segredo:
        return True

    try:
        payload = jwt.decode(token, segredo, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        return False
    except JWTError:
        return False

    sid = str(payload.get("sid") or "")
    if sid != str(sessao_id):
        return False

    return True
