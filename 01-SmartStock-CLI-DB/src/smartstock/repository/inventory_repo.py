from sqlalchemy import select
from sqlalchemy.orm import Session

from smartstock.infra.models import Product, StockMovement


class InventoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_sku(self, sku: str) -> Product | None:
        stmt = select(Product).where(Product.sku == sku)
        return self.session.scalar(stmt)

    def list_all(self) -> list[Product]:
        stmt = select(Product).order_by(Product.sku)
        return list(self.session.scalars(stmt).all())

    def add_product(self, product: Product) -> Product:
        self.session.add(product)
        self.session.flush()
        return product

    def add_movement(self, movement: StockMovement) -> StockMovement:
        self.session.add(movement)
        self.session.flush()
        return movement
