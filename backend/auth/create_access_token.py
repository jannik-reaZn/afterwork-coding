from datetime import datetime, timedelta, timezone

import jwt

from backend.config import Settings


def create_access_token(
    settings: Settings, data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key_jwt, algorithm=settings.algorithm_jwt)
    return encoded_jwt
