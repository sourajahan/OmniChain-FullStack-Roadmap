from sqlalchemy.orm import Session

from smartstock.domain.exceptions import (
    InsufficientStockError,
    InvalidQuantityError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
)
from smartstock.infra.models import Product, StockMovement
from smartstock.repository.inventory_repo import InventoryRepository


class InventoryService:
    def __init__(self, session: Session) -> None:
        self.repo = InventoryRepository(session)

    def create_product(self, sku: str, name: str, initial_quantity: int = 0) -> Product:
        if initial_quantity < 0:
            raise InvalidQuantityError("Initial quantity cannot be negative.")
        if self.repo.get_by_sku(sku) is not None:
            raise ProductAlreadyExistsError(f"Product with SKU '{sku}' already exists.")

        product = Product(sku=sku, name=name, quantity=initial_quantity)
        self.repo.add_product(product)

        if initial_quantity > 0:
            self.repo.add_movement(
                StockMovement(
                    product=product,
                    delta=initial_quantity,
                    reason="initial stock",
                )
            )
        return product

    def adjust_stock(self, sku: str, delta: int, reason: str) -> Product:
        if delta == 0:
            raise InvalidQuantityError("Stock adjustment delta cannot be zero.")

        product = self.repo.get_by_sku(sku)
        if product is None:
            raise ProductNotFoundError(f"Product with SKU '{sku}' not found.")

        new_quantity = product.quantity + delta
        if new_quantity < 0:
            raise InsufficientStockError(
                f"Cannot remove {abs(delta)} units; only {product.quantity} available."
            )

        product.quantity = new_quantity
        self.repo.add_movement(
            StockMovement(product=product, delta=delta, reason=reason)
        )
        return product

    def get_product(self, sku: str) -> Product:
        product = self.repo.get_by_sku(sku)
        if product is None:
            raise ProductNotFoundError(f"Product with SKU '{sku}' not found.")
        return product

    def list_products(self) -> list[Product]:
        return self.repo.list_all()
