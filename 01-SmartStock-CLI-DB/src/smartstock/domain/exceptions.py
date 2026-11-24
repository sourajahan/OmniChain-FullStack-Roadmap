class SmartStockError(Exception):
    """Base exception for SmartStock domain errors."""


class ProductAlreadyExistsError(SmartStockError):
    pass


class ProductNotFoundError(SmartStockError):
    pass


class InsufficientStockError(SmartStockError):
    pass


class InvalidQuantityError(SmartStockError):
    pass
