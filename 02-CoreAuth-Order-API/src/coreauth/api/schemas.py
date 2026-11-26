from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from coreauth.infra.models import OrderStatus, UserRole


class RegisterRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=20, max_length=256)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # noqa: S105


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime


class OrderItemCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    quantity: int = Field(gt=0, le=10_000)
    unit_price: Decimal = Field(ge=Decimal("0.00"), max_digits=12, decimal_places=2)


class OrderCreateRequest(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1, max_length=100)


class OrderStatusUpdateRequest(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    quantity: int
    unit_price: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    items: list[OrderItemResponse]
