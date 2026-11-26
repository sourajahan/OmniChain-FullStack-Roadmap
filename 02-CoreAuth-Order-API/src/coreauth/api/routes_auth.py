from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from coreauth.api.deps import get_current_user, require_roles
from coreauth.api.schemas import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from coreauth.domain.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    TokenReuseDetectedError,
)
from coreauth.infra.db import get_db
from coreauth.infra.models import User, UserRole
from coreauth.service import auth_service

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Annotated[Session, Depends(get_db)]) -> User:
    try:
        return auth_service.register_user(db, email=payload.email, password=payload.password)
    except EmailAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Annotated[Session, Depends(get_db)]) -> TokenResponse:
    try:
        tokens = auth_service.login_user(db, email=payload.email, password=payload.password)
        return TokenResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type,
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Annotated[Session, Depends(get_db)]) -> TokenResponse:
    try:
        tokens = auth_service.refresh_session(db, raw_refresh_token=payload.refresh_token)
        return TokenResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type,
        )
    except (InvalidRefreshTokenError, TokenReuseDetectedError, InvalidCredentialsError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshRequest, db: Annotated[Session, Depends(get_db)]) -> Response:
    auth_service.logout_user(db, raw_refresh_token=payload.refresh_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserResponse)
def me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.get("/admin-only", response_model=dict[str, str])
def admin_only(
    _admin: Annotated[User, Depends(require_roles(UserRole.ADMIN))],
) -> dict[str, str]:
    return {"message": "welcome admin"}
