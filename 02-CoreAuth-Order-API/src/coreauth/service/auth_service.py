from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from coreauth.core.config import settings
from coreauth.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from coreauth.domain.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    TokenReuseDetectedError,
)
from coreauth.infra.models import User, UserRole
from coreauth.repository import auth_repository


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # noqa: S105


def _issue_token_pair(db: Session, user: User, family_id: str | None = None) -> TokenPair:
    fam_id = family_id or uuid4().hex
    raw_refresh = generate_refresh_token()
    expires_at = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)

    auth_repository.create_refresh_token(
        db=db,
        user_id=user.id,
        token_hash=hash_refresh_token(raw_refresh),
        family_id=fam_id,
        expires_at=expires_at,
    )
    access_token = create_access_token(user_id=user.id, role=user.role)
    return TokenPair(access_token=access_token, refresh_token=raw_refresh)


def register_user(
    db: Session,
    email: str,
    password: str,
    role: UserRole = UserRole.CUSTOMER,
) -> User:
    normalized_email = email.strip().lower()
    if auth_repository.get_user_by_email(db, normalized_email) is not None:
        raise EmailAlreadyExistsError("Email is already registered")

    user = auth_repository.create_user(
        db=db,
        email=normalized_email,
        password_hash=hash_password(password),
        role=role,
    )
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str) -> TokenPair:
    normalized_email = email.strip().lower()
    user = auth_repository.get_user_by_email(db, normalized_email)
    if user is None or not user.is_active or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError("Invalid email or password")

    tokens = _issue_token_pair(db, user)
    db.commit()
    return tokens


def refresh_session(db: Session, raw_refresh_token: str) -> TokenPair:
    token_hash = hash_refresh_token(raw_refresh_token)
    stored = auth_repository.get_refresh_token_by_hash(db, token_hash)
    if stored is None:
        raise InvalidRefreshTokenError("Refresh token not found")

    if stored.revoked_at is not None:
        auth_repository.revoke_token_family(db, stored.family_id)
        db.commit()
        raise TokenReuseDetectedError("Refresh token reuse detected; session family revoked")

    now = datetime.now(UTC)
    if stored.expires_at <= now:
        stored.revoked_at = now
        db.commit()
        raise InvalidRefreshTokenError("Refresh token expired")

    user = auth_repository.get_user_by_id(db, stored.user_id)
    if user is None or not user.is_active:
        raise InvalidCredentialsError("User account is inactive")

    stored.revoked_at = now
    tokens = _issue_token_pair(db, user, family_id=stored.family_id)
    db.commit()
    return tokens


def logout_user(db: Session, raw_refresh_token: str) -> None:
    token_hash = hash_refresh_token(raw_refresh_token)
    stored = auth_repository.get_refresh_token_by_hash(db, token_hash)
    if stored is not None and stored.revoked_at is None:
        stored.revoked_at = datetime.now(UTC)
        db.commit()
