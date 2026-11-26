from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from coreauth.infra.models import Order


def list_orders_with_items(
    db: Session,
    customer_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
) -> Sequence[Order]:
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.id.desc())
        .limit(limit)
        .offset(offset)
    )
    if customer_id is not None:
        stmt = stmt.where(Order.customer_id == customer_id)
    return db.scalars(stmt).all()


def get_order_with_items(db: Session, order_id: int) -> Order | None:
    stmt = select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
    return db.scalar(stmt)
