import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from coreauth.core.config import settings
from coreauth.infra.models import UserRole

password_hasher = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    return password_hasher.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return password_hasher.verify(plain_password, password_hash)


def create_access_token(user_id: int, role: UserRole) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role.value,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    payload: dict[str, Any] = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    if payload.get("type") != "access":
        raise jwt.InvalidTokenError("Invalid token type")
    return payload


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
