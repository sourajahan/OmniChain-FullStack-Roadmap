import pytest
from sqlalchemy.exc import IntegrityError

from smartstock.infra.db import SessionLocal
from smartstock.infra.models import Product, StockMovement


def test_create_product_and_movement() -> None:
    with SessionLocal() as session:
        product = Product(sku="TEST-SKU-001", name="Test Widget", quantity=10)
        session.add(product)
        session.flush()

        movement = StockMovement(product_id=product.id, delta=10, reason="initial")
        session.add(movement)
        session.flush()

        assert product.id is not None
        assert movement.id is not None
        assert len(product.movements) == 1

        session.rollback()


def test_negative_quantity_raises_integrity_error() -> None:
    with SessionLocal() as session:
        bad_product = Product(sku="TEST-SKU-NEG", name="Bad Widget", quantity=-5)
        session.add(bad_product)
        with pytest.raises(IntegrityError):
            session.flush()
        session.rollback()
