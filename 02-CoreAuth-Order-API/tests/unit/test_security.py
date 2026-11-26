import pytest
from jwt import InvalidTokenError

from coreauth.core.security import (
    create_access_token,
    decode_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from coreauth.infra.models import UserRole


def test_argon2_password_hashing() -> None:
    hashed = hash_password("StrongPass!123")
    assert hashed != "StrongPass!123"
    assert hashed.startswith("$argon2")
    assert verify_password("StrongPass!123", hashed) is True
    assert verify_password("WrongPass!123", hashed) is False


def test_jwt_access_token_roundtrip() -> None:
    token = create_access_token(user_id=42, role=UserRole.WAREHOUSE)
    payload = decode_access_token(token)
    assert payload["sub"] == "42"
    assert payload["role"] == "warehouse"
    assert payload["type"] == "access"


def test_jwt_rejects_tampered_token() -> None:
    token = create_access_token(user_id=1, role=UserRole.CUSTOMER)
    tampered = token[:-4] + "xxxx"
    with pytest.raises(InvalidTokenError):
        decode_access_token(tampered)


def test_refresh_token_hashing_is_deterministic() -> None:
    raw = generate_refresh_token()
    assert len(raw) >= 48
    assert hash_refresh_token(raw) == hash_refresh_token(raw)
    assert hash_refresh_token(raw) != raw
