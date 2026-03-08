"""
Тесты корректности __tablename__.
"""

from src.shoersshopapi.core.database.models.user import User
from src.shoersshopapi.core.database.models.product import Product
from src.shoersshopapi.core.database.models.brand import Brand
from src.shoersshopapi.core.database.models.order import Order
from src.shoersshopapi.core.database.models.address import Address
from src.shoersshopapi.core.database.models.review import Review
from src.shoersshopapi.core.database.models.favorite import Favorite
from src.shoersshopapi.core.database.models.size import Size
from src.shoersshopapi.core.database.models.cart import Cart
from src.shoersshopapi.core.database.models.association import CartItem, OrderItem


class TestTableNames:

    def test_user(self):
        assert User.__tablename__ == "users"

    def test_product(self):
        assert Product.__tablename__ == "products"

    def test_brand(self):
        assert Brand.__tablename__ == "brands"

    def test_order(self):
        assert Order.__tablename__ == "orders"

    def test_address(self):
        # "Address".endswith("s") → True → "address" + "es" = "addresses"
        assert Address.__tablename__ == "addresses"

    def test_review(self):
        assert Review.__tablename__ == "reviews"

    def test_favorite(self):
        assert Favorite.__tablename__ == "favorites"

    def test_size(self):
        assert Size.__tablename__ == "sizes"

    def test_cart(self):
        assert Cart.__tablename__ == "carts"

    def test_cartitem(self):
        assert CartItem.__tablename__ == "cartitems"

    def test_orderitem(self):
        assert OrderItem.__tablename__ == "orderitems"