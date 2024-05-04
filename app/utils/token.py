from base64 import b64decode

from fastapi.security import OAuth2PasswordBearer
import pyseto

from app.config import config



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/login')

key = pyseto.Key.new(version=4, purpose='local', key=b64decode(config.TOKEN_KEY))


def encode_token(payload: dict) -> bytes:
    return pyseto.encode(key, payload)


def decode_token(token: str | bytes) -> pyseto.Token | None:
    try:
        return pyseto.decode(key, token)
    except Exception:
        return None
