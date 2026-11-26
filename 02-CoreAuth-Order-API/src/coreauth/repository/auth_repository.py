from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from coreauth.infra.models import RefreshToken, User, UserRole


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalar(stmt)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)


def create_user(
    db: Session,
    email: str,
    password_hash: str,
    role: UserRole = UserRole.CUSTOMER,
) -> User:
    user = User(email=email, password_hash=password_hash, role=role)
    db.add(user)
    db.flush()
    return user


def create_refresh_token(
    db: Session,
    user_id: int,
    token_hash: str,
    family_id: str,
    expires_at: datetime,
) -> RefreshToken:
    token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        family_id=family_id,
        expires_at=expires_at,
    )
    db.add(token)
    db.flush()
    return token


def get_refresh_token_by_hash(db: Session, token_hash: str) -> RefreshToken | None:
    stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    return db.scalar(stmt)


def revoke_token_family(db: Session, family_id: str) -> None:
    now = datetime.now(UTC)
    stmt = (
        update(RefreshToken)
        .where(RefreshToken.family_id == family_id, RefreshToken.revoked_at.is_(None))
        .values(revoked_at=now)
    )
    db.execute(stmt)
