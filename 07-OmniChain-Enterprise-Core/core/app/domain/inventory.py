from dataclasses import dataclass


@dataclass
class WarehouseStock:
    warehouse_id: str
    region: str
    sku: str
    available: int
    reserved: int = 0


class InventoryError(Exception):
    pass


class InventoryService:
    """Multi-warehouse inventory with atomic reserve and compensating release."""

    def __init__(self) -> None:
        self._stocks: dict[tuple[str, str], WarehouseStock] = {
            ("WH-EU-1", "SKU-LAPTOP-PRO"): WarehouseStock("WH-EU-1", "EU", "SKU-LAPTOP-PRO", available=20),
            ("WH-US-1", "SKU-LAPTOP-PRO"): WarehouseStock("WH-US-1", "US", "SKU-LAPTOP-PRO", available=15),
            ("WH-EU-1", "SKU-SERVER-RACK"): WarehouseStock("WH-EU-1", "EU", "SKU-SERVER-RACK", available=5),
        }

    def list_stock(self) -> list[dict[str, object]]:
        return [
            {
                "warehouse_id": s.warehouse_id,
                "region": s.region,
                "sku": s.sku,
                "available": s.available,
                "reserved": s.reserved,
            }
            for s in self._stocks.values()
        ]

    def reserve_stock(self, sku: str, quantity: int, preferred_region: str = "EU") -> str:
        if quantity <= 0:
            raise InventoryError("Quantity must be positive.")

        candidates = [s for s in self._stocks.values() if s.sku == sku and s.available >= quantity]
        if not candidates:
            raise InventoryError(f"Insufficient stock for SKU {sku} (requested {quantity}).")

        candidates.sort(key=lambda s: (0 if s.region == preferred_region else 1, -s.available))
        chosen = candidates[0]
        chosen.available -= quantity
        chosen.reserved += quantity
        return chosen.warehouse_id

    def release_stock(self, warehouse_id: str, sku: str, quantity: int) -> None:
        stock = self._stocks.get((warehouse_id, sku))
        if not stock:
            return
        release_qty = min(quantity, stock.reserved)
        stock.reserved -= release_qty
        stock.available += release_qty
