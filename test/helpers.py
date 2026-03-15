"""
Общие утилиты, Pydantic-схемы и CRUD-классы для тестов.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel

from shoersshopapi.core.database.models import (
    User,
    Product,
    Brand,
    Order,
    Address,
    Review,
    Favorite,
    Size,
    Cart,
    CartItem,
    OrderItem
)

from shoersshopapi.api.v1.basecrud import BaseCrud

from shoersshopapi.core.utils.enum import (
    Role,
    Status,
    Color,
    Rating
)


# ═══════════════════════════════════════
#  Утилиты
# ═══════════════════════════════════════

def gen_id() -> str:
    return str(uuid.uuid4())


def unique_phone() -> str:
    return f"+7{uuid.uuid4().hex[:10]}"


def unique_email() -> str:
    return f"test_{uuid.uuid4().hex[:8]}@test.com"


# ═══════════════════════════════════════
#  Pydantic-схемы
# ═══════════════════════════════════════

class UserCreate(BaseModel):
    id: str
    surname: str
    name: str
    patronymic: str
    password: bytes
    phone: str
    email: str
    social_link: list[str] | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    phone: str | None = None
    email: str | None = None
    social_link: list[str] | None = None


class BrandCreate(BaseModel):
    id: str
    brand_logo: str


class BrandUpdate(BaseModel):
    brand_logo: str | None = None


class ProductCreate(BaseModel):
    id: str
    title: str
    price: float
    color: Color
    avg_grade: str
    brand_id: str | None = None


class ProductUpdate(BaseModel):
    title: str | None = None
    price: float | None = None
    avg_grade: str | None = None


class AddressCreate(BaseModel):
    id: str
    user_id: str
    region: str
    city: str
    street: str
    house: str
    entrance: str
    apartment: str
    postcode: int


class AddressUpdate(BaseModel):
    city: str | None = None
    street: str | None = None
    postcode: int | None = None


class OrderCreate(BaseModel):
    id: str
    user_id: str
    address_id: str
    order_date: datetime
    total_amount: int


class OrderUpdate(BaseModel):
    total_amount: int | None = None
    status: Status | None = None


class ReviewCreate(BaseModel):
    id: str
    user_id: str
    comment_text: str
    rating: Rating | None = None


class ReviewUpdate(BaseModel):
    comment_text: str | None = None
    rating: Rating | None = None


class FavoriteCreate(BaseModel):
    id: str
    user_id: str
    product_id: str


class SizeCreate(BaseModel):
    id: str
    product_id: str
    count: int
    size: int


class SizeUpdate(BaseModel):
    count: int | None = None
    size: int | None = None


class CartCreate(BaseModel):
    id: str
    user_id: str


class CartItemCreate(BaseModel):
    id: str
    cart_id: str
    product_id: str
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int | None = None


class OrderItemCreate(BaseModel):
    id: str
    order_id: str
    product_id: str
    quantity: int


class OrderItemUpdate(BaseModel):
    quantity: int | None = None


# ═══════════════════════════════════════
#  CRUD-классы
# ═══════════════════════════════════════

class UserCrud(BaseCrud[User]):
    model = User


class BrandCrud(BaseCrud[Brand]):
    model = Brand


class ProductCrud(BaseCrud[Product]):
    model = Product


class OrderCrud(BaseCrud[Order]):
    model = Order


class AddressCrud(BaseCrud[Address]):
    model = Address


class ReviewCrud(BaseCrud[Review]):
    model = Review


class FavoriteCrud(BaseCrud[Favorite]):
    model = Favorite


class SizeCrud(BaseCrud[Size]):
    model = Size


class CartCrud(BaseCrud[Cart]):
    model = Cart


class CartItemCrud(BaseCrud[CartItem]):
    model = CartItem


class OrderItemCrud(BaseCrud[OrderItem]):
    model = OrderItem