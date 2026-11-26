from decimal import Decimal
from typing import Any
from uuid import uuid4

from sqlalchemy import event

from coreauth.infra.db import SessionLocal, engine
from coreauth.infra.models import Order, OrderItem, OrderStatus, User, UserRole
from coreauth.repository.order_repository import list_orders_with_items


def test_list_orders_prevents_n_plus_one() -> None:
    db = SessionLocal()
    email = f"nplus1-{uuid4().hex[:8]}@example.com"
    created_order_ids: list[int] = []
    user_id: int | None = None

    try:
        user = User(email=email, password_hash="hashed", role=UserRole.CUSTOMER)
        db.add(user)
        db.flush()
        user_id = user.id

        for i in range(5):
            order = Order(
                customer_id=user.id,
                status=OrderStatus.PENDING,
                total_amount=Decimal("200.00"),
                items=[
                    OrderItem(sku=f"SKU-{i}-A", quantity=1, unit_price=Decimal("100.00")),
                    OrderItem(sku=f"SKU-{i}-B", quantity=1, unit_price=Decimal("100.00")),
                ],
            )
            db.add(order)
            db.flush()
            created_order_ids.append(order.id)
        db.commit()
        db.expunge_all()

        query_count = 0

        def count_queries(
            _conn: Any,
            _cursor: Any,
            _statement: Any,
            _parameters: Any,
            _context: Any,
            _executemany: Any,
        ) -> None:
            nonlocal query_count
            query_count += 1

        event.listen(engine, "before_cursor_execute", count_queries)
        try:
            orders = list_orders_with_items(db, customer_id=user_id, limit=10)
            total_items = sum(len(order.items) for order in orders)
        finally:
            event.remove(engine, "before_cursor_execute", count_queries)

        assert len(orders) == 5
        assert total_items == 10
        assert query_count <= 2
    finally:
        db.rollback()
        if created_order_ids:
            db.query(Order).filter(Order.id.in_(created_order_ids)).delete(
                synchronize_session=False
            )
        if user_id is not None:
            db.query(User).filter(User.id == user_id).delete(synchronize_session=False)
        db.commit()
        db.close()
