from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy.orm import Session

from coreauth.domain.exceptions import (
    InvalidOrderTransitionError,
    OrderAccessDeniedError,
    OrderNotFoundError,
)
from coreauth.infra.models import Order, OrderItem, OrderStatus, User, UserRole
from coreauth.repository import order_repository

ALLOWED_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING: {OrderStatus.PAID, OrderStatus.CANCELLED},
    OrderStatus.PAID: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
    OrderStatus.SHIPPED: set(),
    OrderStatus.CANCELLED: set(),
}


@dataclass(frozen=True)
class OrderItemInput:
    sku: str
    quantity: int
    unit_price: Decimal


def create_order(
    db: Session,
    customer: User,
    items: Sequence[OrderItemInput],
) -> Order:
    total = sum((item.unit_price * item.quantity for item in items), Decimal("0.00"))
    order = Order(
        customer_id=customer.id,
        status=OrderStatus.PENDING,
        total_amount=total,
        items=[
            OrderItem(sku=item.sku, quantity=item.quantity, unit_price=item.unit_price)
            for item in items
        ],
    )
    order_repository.create_order(db, order)
    db.commit()
    db.refresh(order)
    return order


def list_orders(
    db: Session,
    actor: User,
    status: OrderStatus | None = None,
    limit: int = 20,
    offset: int = 0,
) -> Sequence[Order]:
    customer_id = actor.id if actor.role == UserRole.CUSTOMER else None
    return order_repository.list_orders_with_items(
        db=db,
        customer_id=customer_id,
        status=status,
        limit=limit,
        offset=offset,
    )


def get_order(db: Session, actor: User, order_id: int) -> Order:
    order = order_repository.get_order_with_items(db, order_id)
    if order is None:
        raise OrderNotFoundError(f"Order {order_id} not found")
    if actor.role == UserRole.CUSTOMER and order.customer_id != actor.id:
        raise OrderAccessDeniedError("You do not have permission to view this order")
    return order


def update_order_status(
    db: Session,
    order_id: int,
    new_status: OrderStatus,
) -> Order:
    order = order_repository.get_order_with_items(db, order_id)
    if order is None:
        raise OrderNotFoundError(f"Order {order_id} not found")

    if new_status not in ALLOWED_TRANSITIONS[order.status]:
        raise InvalidOrderTransitionError(
            f"Cannot transition order from '{order.status.value}' to '{new_status.value}'"
        )

    order.status = new_status
    db.commit()
    db.refresh(order)
    return order
