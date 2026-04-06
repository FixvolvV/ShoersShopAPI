from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    declared_attr,
    mapped_column,
    relationship
)
from sqlalchemy import ForeignKey

from sqlalchemy.orm.relationships import _LazyLoadArgumentType

if TYPE_CHECKING:
    from .user import User
    from .product import Product

class UserRelationMixin:
    _user_id_nullable: bool = False
    _user_id_unique: bool = False
    _user_back_populates: str | None = None
    _user_load_strategy: _LazyLoadArgumentType = "noload"

    @declared_attr
    def user_id(cls) -> Mapped[str]:
        return mapped_column(
            ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
            unique=cls._user_id_unique,
            nullable=cls._user_id_nullable
        )
    
    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship (
            "User",
            back_populates=cls._user_back_populates,
            lazy=cls._user_load_strategy,
        )

class ProductRelationMixin:
    _product_id_nullable: bool = False
    _product_id_unique: bool = False
    _product_back_populates: str | None = None
    _product_load_strategy: _LazyLoadArgumentType = "noload"

    @declared_attr
    def product_id(cls) -> Mapped[str]:
        return mapped_column(
            ForeignKey("products.id", onupdate="CASCADE", ondelete="CASCADE"),
            unique=cls._product_id_unique,
            nullable=cls._product_id_nullable
        )
    
    @declared_attr
    def product(cls) -> Mapped["Product"]:
        return relationship (
            "Product",
            back_populates=cls._product_back_populates,
            lazy=cls._product_load_strategy,
        )