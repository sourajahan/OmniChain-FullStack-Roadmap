import pytest

from smartstock.domain.exceptions import (
    InsufficientStockError,
    InvalidQuantityError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
)
from smartstock.infra.db import SessionLocal
from smartstock.service.inventory_service import InventoryService


def test_create_and_adjust_stock() -> None:
    with SessionLocal() as session:
        service = InventoryService(session)

        product = service.create_product(sku="LAP-001", name="Laptop", initial_quantity=5)
        assert product.quantity == 5
        assert len(product.movements) == 1

        service.adjust_stock(sku="LAP-001", delta=3, reason="restock")
        assert product.quantity == 8

        service.adjust_stock(sku="LAP-001", delta=-4, reason="sale")
        assert product.quantity == 4
        assert len(product.movements) == 3

        session.rollback()


def test_duplicate_sku_raises_error() -> None:
    with SessionLocal() as session:
        service = InventoryService(session)
        service.create_product(sku="DUP-001", name="Item A")
        with pytest.raises(ProductAlreadyExistsError):
            service.create_product(sku="DUP-001", name="Item B")
        session.rollback()


def test_insufficient_stock_raises_error() -> None:
    with SessionLocal() as session:
        service = InventoryService(session)
        service.create_product(sku="LOW-001", name="Mouse", initial_quantity=2)
        with pytest.raises(InsufficientStockError):
            service.adjust_stock(sku="LOW-001", delta=-5, reason="sale")
        session.rollback()


def test_missing_product_and_invalid_quantity() -> None:
    with SessionLocal() as session:
        service = InventoryService(session)
        with pytest.raises(ProductNotFoundError):
            service.get_product("DOES-NOT-EXIST")
        with pytest.raises(InvalidQuantityError):
            service.create_product(sku="BAD-001", name="Bad", initial_quantity=-1)
        session.rollback()
