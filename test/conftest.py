from typing import AsyncGenerator, AsyncIterator
from datetime import datetime, timezone

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

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

from shoersshopapi.core.utils.enum import (
    Role,
    Status,
    Color,
    Rating
)

from .helpers import gen_id, unique_phone, unique_email

from shoersshopapi.core.settings import settings

import pytest

# ═══════════════════════════════════════
#  Engine + Session
# ═══════════════════════════════════════

@pytest.fixture(scope="function")
def test_engine():
    """Синхронная фикстура — просто создаёт engine, без event loop."""
    engine = create_async_engine(
        url=str(settings.db.url),
        echo=False,
    )
    return engine


@pytest.fixture(scope="function")
def test_session_factory(test_engine: AsyncEngine):
    """Синхронная фикстура — фабрика сессий."""
    return async_sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


@pytest_asyncio.fixture(scope="function")
async def session(test_session_factory, test_engine):
    """
    Сессия с автоматическим rollback.
    Вся работа (setup + yield + teardown) в одной async-функции
    на одном event loop.
    """
    sess = test_session_factory()
    try:
        yield sess
    finally:
        await sess.rollback()
        await sess.close()
        await test_engine.dispose()


# ═══════════════════════════════════════
#  Фабрики тестовых объектов
# ═══════════════════════════════════════

@pytest_asyncio.fixture
async def sample_user(session: AsyncSession) -> User:
    user = User(
        id=gen_id(),
        surname="Тестов",
        name="Тест",
        patronymic="Тестович",
        password=b"hashed_password_bytes",
        phone=unique_phone(),
        email=unique_email(),
    )
    session.add(user)
    await session.flush()
    return user


@pytest_asyncio.fixture
async def sample_brand(session: AsyncSession) -> Brand:
    brand = Brand(
        id=gen_id(),
        brand_logo="https://example.com/nike_logo.png",
    )
    session.add(brand)
    await session.flush()
    return brand


@pytest_asyncio.fixture
async def sample_product(session: AsyncSession, sample_brand: Brand) -> Product:
    product = Product(
        id=gen_id(),
        brand_id=sample_brand.id,
        title="Air Max 90",
        price=12990.0,
        color=Color.white,
        avg_grade="4.5",
    )
    session.add(product)
    await session.flush()
    return product


@pytest_asyncio.fixture
async def sample_address(session: AsyncSession, sample_user: User) -> Address:
    address = Address(
        id=gen_id(),
        user_id=sample_user.id,
        region="Московская область",
        city="Москва",
        street="Тверская",
        house="1",
        entrance="2",
        apartment="15",
        postcode=123456,
    )
    session.add(address)
    await session.flush()
    return address


@pytest_asyncio.fixture
async def sample_order(session: AsyncSession, sample_user: User, sample_address: Address) -> Order:
    order = Order(
        id=gen_id(),
        user_id=sample_user.id,
        address_id=sample_address.id,
        order_date=datetime.now(timezone.utc).replace(tzinfo=None),
        total_amount=25980,
    )
    session.add(order)
    await session.flush()
    return order


@pytest_asyncio.fixture
async def sample_cart(session: AsyncSession, sample_user: User) -> Cart:
    cart = Cart(id=gen_id(), user_id=sample_user.id)
    session.add(cart)
    await session.flush()
    return cart


@pytest_asyncio.fixture
async def sample_review(session: AsyncSession, sample_user: User) -> Review:
    review = Review(
        id=gen_id(),
        user_id=sample_user.id,
        comment_text="Отличные кроссовки!",
        rating=Rating.very_good,
    )
    session.add(review)
    await session.flush()
    return review


@pytest_asyncio.fixture
async def sample_favorite(session: AsyncSession, sample_user: User, sample_product: Product) -> Favorite:
    fav = Favorite(id=gen_id(), user_id=sample_user.id, product_id=sample_product.id)
    session.add(fav)
    await session.flush()
    return fav


@pytest_asyncio.fixture
async def sample_size(session: AsyncSession, sample_product: Product) -> Size:
    size = Size(id=gen_id(), product_id=sample_product.id, count=10, size=42)
    session.add(size)
    await session.flush()
    return size


@pytest_asyncio.fixture
async def sample_cart_item(session: AsyncSession, sample_cart: Cart, sample_product: Product) -> CartItem:
    ci = CartItem(id=gen_id(), cart_id=sample_cart.id, product_id=sample_product.id, quantity=2)
    session.add(ci)
    await session.flush()
    return ci


@pytest_asyncio.fixture
async def sample_order_item(session: AsyncSession, sample_order: Order, sample_product: Product) -> OrderItem:
    oi = OrderItem(id=gen_id(), order_id=sample_order.id, product_id=sample_product.id, quantity=3)
    session.add(oi)
    await session.flush()
    return oi


# ═══════════════════════════════════════
#  Множественные фабрики (для тестов списков)
# ═══════════════════════════════════════

@pytest_asyncio.fixture
async def sample_users(session: AsyncSession) -> list[User]:
    """Создаёт 5 пользователей"""
    users = []
    for i in range(5):
        user = User(
            id=gen_id(),
            surname=f"Фамилия_{i}",
            name=f"Имя_{i}",
            patronymic=f"Отчество_{i}",
            password=b"hashed_password_bytes",
            phone=unique_phone(),
            email=unique_email(),
        )
        session.add(user)
        users.append(user)
    await session.flush()
    return users


@pytest_asyncio.fixture
async def user_with_addresses(
    session: AsyncSession,
    sample_user: User
) -> tuple[User, list[Address]]:
    """Пользователь + 3 адреса"""
    addresses = []
    for i in range(3):
        addr = Address(
            id=gen_id(),
            user_id=sample_user.id,
            region=f"Регион_{i}",
            city=f"Город_{i}",
            street=f"Улица_{i}",
            house=str(i + 1),
            entrance=str(i + 1),
            apartment=str(i + 10),
            postcode=100000 + i,
        )
        session.add(addr)
        addresses.append(addr)

    await session.flush()
    return sample_user, addresses

@pytest_asyncio.fixture
async def user_with_reviews(
    session: AsyncSession,
    sample_user: User
) -> tuple[User, list[Review]]:
    """Пользователь + 3 отзыва"""
    reviews = []
    for i in range(3):
        review = Review(
            id=gen_id(),
            user_id=sample_user.id,
            comment_text=f"Отзыв_{i}",
            rating=Rating.very_good,
        )
        session.add(review)
        reviews.append(review)
    await session.flush()
    return sample_user, reviews

@pytest_asyncio.fixture
async def user_with_orders(
    session: AsyncSession,
    sample_user: User,
) -> tuple[User, list[Order]]:
    """Пользователь + 3 заказа"""
    # Сначала создаём адрес
    address = Address(
        id=gen_id(),
        user_id=sample_user.id,
        region="Регион",
        city="Город",
        street="Улица",
        house="1",
        entrance="1",
        apartment="1",
        postcode=100000,
    )
    session.add(address)
    await session.flush()

    orders = []
    for i in range(3):
        order = Order(
            id=gen_id(),
            user_id=sample_user.id,
            address_id=address.id,
            order_date=datetime.now(timezone.utc).replace(tzinfo=None),
            total_amount=10000 * (i + 1),
        )
        session.add(order)
        orders.append(order)
    await session.flush()
    return sample_user, orders