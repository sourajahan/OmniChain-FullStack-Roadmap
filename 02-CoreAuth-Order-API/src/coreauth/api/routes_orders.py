from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from coreauth.api.deps import get_current_user, require_roles
from coreauth.api.schemas import (
    OrderCreateRequest,
    OrderResponse,
    OrderStatusUpdateRequest,
)
from coreauth.domain.exceptions import (
    InvalidOrderTransitionError,
    OrderAccessDeniedError,
    OrderNotFoundError,
)
from coreauth.infra.db import get_db
from coreauth.infra.models import Order, OrderStatus, User, UserRole
from coreauth.service import order_service

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreateRequest,
    customer: Annotated[User, Depends(require_roles(UserRole.CUSTOMER))],
    db: Annotated[Session, Depends(get_db)],
) -> Order:
    items = [
        order_service.OrderItemInput(
            sku=item.sku,
            quantity=item.quantity,
            unit_price=item.unit_price,
        )
        for item in payload.items
    ]
    return order_service.create_order(db=db, customer=customer, items=items)


@router.get("", response_model=list[OrderResponse])
def list_orders(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    order_status: Annotated[OrderStatus | None, Query(alias="status")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Sequence[Order]:
    return order_service.list_orders(
        db=db,
        actor=current_user,
        status=order_status,
        limit=limit,
        offset=offset,
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Order:
    try:
        return order_service.get_order(db=db, actor=current_user, order_id=order_id)
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except OrderAccessDeniedError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdateRequest,
    _staff: Annotated[User, Depends(require_roles(UserRole.WAREHOUSE, UserRole.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
) -> Order:
    try:
        return order_service.update_order_status(
            db=db,
            order_id=order_id,
            new_status=payload.status,
        )
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidOrderTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
