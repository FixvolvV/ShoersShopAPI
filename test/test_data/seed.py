"""
Скрипт для заполнения сервера тестовыми данными.
Порядок создания: Users → Brands → Products → Addresses → Cart Items → Orders
"""

import requests
import sys
from datetime import datetime, timedelta
from random import uniform

BASE_URL = "http://localhost:8000/api/v1"


def log_response(entity_name: str, response: requests.Response) -> dict | None:
    """Логирует результат запроса и возвращает JSON ответа."""
    if response.status_code in (200, 201):
        data = response.json()
        entity_id = data.get("id", "N/A")
        print(f"  ✅ {entity_name} создан (id: {entity_id})")
        return data
    else:
        print(f"  ❌ {entity_name} — ошибка {response.status_code}: {response.text}")
        return None


# ========================== ТЕСТОВЫЕ ДАННЫЕ ==========================

USERS = [
    {
        "phone": "+79001112233",
        "email": "ivan.petrov@mail.ru",
        "surname": "Петров",
        "name": "Иван",
        "patronymic": "Сергеевич",
        "password": "password123",
        "role": "user",
    },
    {
        "phone": "+79002223344",
        "email": "anna.smirnova@mail.ru",
        "surname": "Смирнова",
        "name": "Анна",
        "patronymic": "Дмитриевна",
        "password": "password456",
        "role": "user",
    },
    {
        "phone": "+79003334455",
        "email": "oleg.kozlov@mail.ru",
        "surname": "Козлов",
        "name": "Олег",
        "patronymic": "Владимирович",
        "password": "password789",
        "role": "user",
    },
    {
        "phone": "+79004445566",
        "email": "maria.ivanova@mail.ru",
        "surname": "Иванова",
        "name": "Мария",
        "patronymic": "Александровна",
        "password": "adminpass",
        "role": "admin",
    },
    {
        "phone": "+79005556677",
        "email": "dmitry.volkov@mail.ru",
        "surname": "Волков",
        "name": "Дмитрий",
        "patronymic": "Игоревич",
        "password": "passw0rd",
        "role": "user",
    },
]

BRANDS = [
    {"name": "Nike", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Logo_NIKE.svg/200px-Logo_NIKE.svg.png"},
    {"name": "Adidas", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Adidas_Logo.svg/200px-Adidas_Logo.svg.png"},
    {"name": "Puma", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Puma_AG.svg/200px-Puma_AG.svg.png"},
    {"name": "Reebok", "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Reebok_2019_logo.svg/200px-Reebok_2019_logo.svg.png"},
]

# Продукты — brand_id подставляется после создания брендов
PRODUCTS_TEMPLATES = [
    # Nike (brand index 0)
    {"title": "Air Max 90", "price": 12990.0, "color": "black"},
    {"title": "Air Force 1", "price": 10990.0, "color": "white"},
    {"title": "React Vision", "price": 14490.0, "color": "blue"},
    # Adidas (brand index 1)
    {"title": "Ultraboost 22", "price": 15990.0, "color": "black"},
    {"title": "Stan Smith", "price": 8990.0, "color": "white"},
    {"title": "Gazelle", "price": 9490.0, "color": "gray"},
    # Puma (brand index 2)
    {"title": "RS-X", "price": 11990.0, "color": "blue"},
    {"title": "Suede Classic", "price": 7490.0, "color": "black"},
    {"title": "Cali Star", "price": 8990.0, "color": "white"},
    # Reebok (brand index 3)
    {"title": "Classic Leather", "price": 7990.0, "color": "white"},
    {"title": "Club C 85", "price": 8490.0, "color": "gray"},
    {"title": "Nano X2", "price": 12990.0, "color": "black"},
]

# Индекс бренда → индексы его продуктов
BRAND_PRODUCT_MAP = {
    0: [0, 1, 2],
    1: [3, 4, 5],
    2: [6, 7, 8],
    3: [9, 10, 11],
}

# Шаблоны адресов
ADDRESSES_TEMPLATES = [
    {
        "region": "Московская область",
        "city": "Москва",
        "street": "ул. Тверская",
        "house": "12",
        "entrance": "2",
        "apartment": "45",
        "postcode": 125009,
    },
    {
        "region": "Ленинградская область",
        "city": "Санкт-Петербург",
        "street": "Невский проспект",
        "house": "78",
        "entrance": "1",
        "apartment": "12",
        "postcode": 191025,
    },
    {
        "region": "Новосибирская область",
        "city": "Новосибирск",
        "street": "ул. Ленина",
        "house": "33",
        "entrance": "3",
        "apartment": "101",
        "postcode": 630099,
    },
    {
        "region": "Свердловская область",
        "city": "Екатеринбург",
        "street": "ул. Малышева",
        "house": "51",
        "entrance": "1",
        "apartment": "7",
        "postcode": 620000,
    },
    {
        "region": "Краснодарский край",
        "city": "Краснодар",
        "street": "ул. Красная",
        "house": "100",
        "entrance": "4",
        "apartment": "88",
        "postcode": 350000,
    },
    {
        "region": "Московская область",
        "city": "Москва",
        "street": "ул. Арбат",
        "house": "20",
        "entrance": "1",
        "apartment": "3",
        "postcode": 119002,
    },
]

# Индекс пользователя → индексы его адресов
USER_ADDRESS_MAP = {
    0: [0, 5],  # 2 адреса
    1: [1],
    2: [2],
    3: [3],
    4: [4],
}

# Товары в корзину: (индекс_пользователя, индекс_продукта, количество)
CART_ITEMS = [
    (0, 0, 2),   # Иван: Air Max 90 x2
    (0, 4, 1),   # Иван: Stan Smith x1
    (0, 7, 1),   # Иван: Suede Classic x1
    (1, 1, 1),   # Анна: Air Force 1 x1
    (1, 9, 2),   # Анна: Classic Leather x2
    (2, 3, 1),   # Олег: Ultraboost 22 x1
    (2, 6, 3),   # Олег: RS-X x3
    (4, 11, 1),  # Дмитрий: Nano X2 x1
    (4, 2, 1),   # Дмитрий: React Vision x1
]

# Шаблоны заказов
ORDERS_TEMPLATES = [
    {"user_idx": 0, "address_local_idx": 0, "status": "delivered", "days_ago": 14},
    {"user_idx": 1, "address_local_idx": 0, "status": "transit", "days_ago": 3},
    {"user_idx": 2, "address_local_idx": 0, "status": "confirmation", "days_ago": 0},
    {"user_idx": 0, "address_local_idx": 1, "status": "cancelled", "days_ago": 7},
    {"user_idx": 4, "address_local_idx": 0, "status": "transit", "days_ago": 2},
]


# ========================== СОЗДАНИЕ ДАННЫХ ==========================

def create_users() -> list[dict]:
    print("\n📌 Создание пользователей...")
    created = []
    for user in USERS:
        resp = requests.post(f"{BASE_URL}/users/", json=user)
        result = log_response(f"User {user['email']}", resp)
        if result:
            created.append(result)
        else:
            sys.exit(1)
    return created


import io


def create_dummy_logo(brand_name: str) -> io.BytesIO:
    """Создаёт минимальный PNG-файл как заглушку логотипа."""
    # Минимальный валидный 1x1 PNG
    import struct
    import zlib

    def create_minimal_png() -> bytes:
        signature = b'\x89PNG\r\n\x1a\n'

        # IHDR
        ihdr_data = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
        ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
        ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)

        # IDAT
        raw_data = zlib.compress(b'\x00\xff\xff\xff')
        idat_crc = zlib.crc32(b'IDAT' + raw_data) & 0xffffffff
        idat = struct.pack('>I', len(raw_data)) + b'IDAT' + raw_data + struct.pack('>I', idat_crc)

        # IEND
        iend_crc = zlib.crc32(b'IEND') & 0xffffffff
        iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)

        return signature + ihdr + idat + iend

    buf = io.BytesIO(create_minimal_png())
    buf.name = f"{brand_name.lower()}_logo.png"
    return buf


def create_brands() -> list[dict]:
    print("\n📌 Создание брендов...")
    created = []
    for brand in BRANDS:
        # Пытаемся скачать реальный логотип, если не получится — заглушка
        try:
            img_resp = requests.get(brand["logo_url"], timeout=5)
            if img_resp.status_code == 200:
                logo_file = io.BytesIO(img_resp.content)
                logo_file.name = f"{brand['name'].lower()}_logo.png"
            else:
                logo_file = create_dummy_logo(brand["name"])
        except Exception:
            logo_file = create_dummy_logo(brand["name"])

        resp = requests.post(
            f"{BASE_URL}/brands/",
            params={"name": brand["name"]},
            files={"logo": (logo_file.name, logo_file, "image/png")},
        )
        result = log_response(f"Brand {brand['name']}", resp)
        if result:
            created.append(result)
        else:
            sys.exit(1)
    return created


def create_products(brand_ids: list[str]) -> list[dict]:
    print("\n📌 Создание продуктов...")
    created = []
    for brand_idx, product_indices in BRAND_PRODUCT_MAP.items():
        brand_id = brand_ids[brand_idx]
        for prod_idx in product_indices:
            product = PRODUCTS_TEMPLATES[prod_idx].copy()
            product["brand_id"] = brand_id
            resp = requests.post(f"{BASE_URL}/products/", json=product)
            result = log_response(f"Product '{product['title']}'", resp)
            if result:
                created.append(result)
            else:
                sys.exit(1)
    return created


def create_addresses(user_ids: list[str]) -> dict[int, list[str]]:
    print("\n📌 Создание адресов...")
    user_address_ids: dict[int, list[str]] = {}

    for user_idx in sorted(USER_ADDRESS_MAP.keys()):
        user_id = user_ids[user_idx]
        user_address_ids[user_idx] = []

        for addr_idx in USER_ADDRESS_MAP[user_idx]:
            address = ADDRESSES_TEMPLATES[addr_idx].copy()
            # Убираем user_id из body — он идёт в query
            address.pop("user_id", None)

            resp = requests.post(
                f"{BASE_URL}/addresses/",
                params={"user_id": user_id},  # user_id в query
                json=address,                  # остальное в body
            )
            result = log_response(
                f"Address: user {user_idx} → {address['city']}, {address['street']}",
                resp,
            )
            if result:
                user_address_ids[user_idx].append(result["id"])
            else:
                sys.exit(1)

    return user_address_ids


def add_cart_items(user_ids: list[str], product_ids: list[str]) -> None:
    print("\n📌 Добавление товаров в корзины...")
    for user_idx, prod_idx, quantity in CART_ITEMS:
        user_id = user_ids[user_idx]
        product_id = product_ids[prod_idx]
        item_data = {
            "product_id": product_id,
            "quantity": quantity,
        }
        resp = requests.post(f"{BASE_URL}/carts/{user_id}/items", json=item_data)
        product_title = PRODUCTS_TEMPLATES[prod_idx]["title"]
        log_response(
            f"CartItem: user {user_idx} ← '{product_title}' x{quantity}",
            resp,
        )


def create_orders(
    user_ids: list[str],
    user_address_ids: dict[int, list[str]],
) -> list[dict]:
    print("\n📌 Создание заказов...")
    created = []

    for order_tmpl in ORDERS_TEMPLATES:
        user_idx = order_tmpl["user_idx"]
        addr_local_idx = order_tmpl["address_local_idx"]
        user_id = user_ids[user_idx]
        address_id = user_address_ids[user_idx][addr_local_idx]

        order_date = datetime.now().replace(tzinfo=None) - timedelta(days=order_tmpl["days_ago"])

        order_data = {
            "address_id": address_id,
            # user_id убран из body
            "order_date": order_date.isoformat(),
            "total_amount": round(uniform(5000, 50000), 2),
            "status": order_tmpl["status"],
        }

        resp = requests.post(
            f"{BASE_URL}/orders/",
            params={"user_id": user_id},  # user_id только в query
            json=order_data,
        )
        result = log_response(
            f"Order: user {user_idx}, status={order_tmpl['status']}",
            resp,
        )
        if result:
            created.append(result)

    return created

# ========================== MAIN ==========================

def main():
    print("=" * 60)
    print("🚀 Запуск скрипта заполнения тестовыми данными")
    print(f"   Сервер: {BASE_URL}")
    print("=" * 60)

    # Проверка доступности сервера
    try:
        requests.get(f"{BASE_URL}/users/", timeout=5)
    except requests.ConnectionError:
        print(f"\n❌ Сервер {BASE_URL} недоступен!")
        sys.exit(1)

    # 1. Пользователи
    users = create_users()
    user_ids = [u["id"] for u in users]

    # 2. Бренды
    brands = create_brands()
    brand_ids = [b["id"] for b in brands]

    # 3. Продукты
    products = create_products(brand_ids)
    product_ids = [p["id"] for p in products]

    # 4. Адреса
    user_address_ids = create_addresses(user_ids)

    # 5. Корзины
    add_cart_items(user_ids, product_ids)

    # 6. Заказы
    orders = create_orders(user_ids, user_address_ids)

    # Подсчёт адресов
    total_addresses = sum(len(v) for v in user_address_ids.values())

    # Итог
    print("\n" + "=" * 60)
    print("✅ Тестовые данные успешно созданы!")
    print(f"   👤 Пользователей:      {len(users)}")
    print(f"   🏷️  Брендов:             {len(brands)}")
    print(f"   📦 Продуктов:           {len(products)}")
    print(f"   🏠 Адресов:             {total_addresses}")
    print(f"   🛒 Товаров в корзинах:  {len(CART_ITEMS)}")
    print(f"   📋 Заказов:             {len(orders)}")
    print("=" * 60)


if __name__ == "__main__":
    main()