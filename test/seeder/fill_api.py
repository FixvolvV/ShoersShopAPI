import requests
import json
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random

# Конфигурация
BASE_URL = "http://localhost:8000"  # Измените на ваш URL
API_BASE = f"{BASE_URL}/api/v1"

# Данные для авторизации
ADMIN_USERNAME = "+777"
ADMIN_PASSWORD = "FixvolvV1234"

# Путь к папке с изображениями
IMAGES_DIR = Path("images")
BRANDS_IMAGES_DIR = IMAGES_DIR / "brands"
PRODUCTS_IMAGES_DIR = IMAGES_DIR / "products"


class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        
    def login(self):
        """Авторизация и получение токена"""
        response = self.session.post(
            f"{API_BASE}/auth/login",
            data={
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
        )
        response.raise_for_status()
        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}"
        })
        print("✓ Успешная авторизация")
        
    def create_brand(self, name, logo_path=None):
        """Создание бренда"""
        # Пытаемся загрузить изображение из файла
        if logo_path and Path(logo_path).exists():
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
            print(f"  Загружено изображение: {logo_path}")
        else:
            # Создаем изображение с текстом
            logo_data = self._generate_brand_logo(name)
            print(f"  Создано автоматическое изображение для {name}")
            
        files = {
            'logo': ('logo.png', BytesIO(logo_data), 'image/png')
        }
        params = {'name': name}
        
        response = self.session.post(
            f"{API_BASE}/brands/",
            params=params,
            files=files
        )
        response.raise_for_status()
        brand = response.json()
        print(f"✓ Создан бренд: {name} (ID: {brand['id']})")
        return brand
    
    def _generate_brand_logo(self, brand_name):
        """Генерация логотипа бренда"""
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
        color = random.choice(colors)
        
        img = Image.new('RGB', (300, 300), color=color)
        draw = ImageDraw.Draw(img)
        
        # Добавляем текст
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
            
        text = brand_name[:2].upper()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((300 - text_width) // 2, (300 - text_height) // 2)
        draw.text(position, text, fill='white', font=font)
        
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
        
    def create_product(self, brand_id, title, price, color, article, category, avg_grade=4.5):
        """Создание продукта"""
        data = {
            "brand_id": brand_id,
            "title": title,
            "price": price,
            "color": color,
            "article": article,
            "category": category,
            "avg_grade": avg_grade
        }
        
        response = self.session.post(
            f"{API_BASE}/products/",
            json=data
        )
        response.raise_for_status()
        product = response.json()
        print(f"✓ Создан продукт: {title} (ID: {product['id']})")
        return product
    
    def update_product_logo(self, product_id, logo_path=None, product_title=""):
        """Обновление логотипа продукта"""
        if logo_path and Path(logo_path).exists():
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
            print(f"  Загружено изображение: {logo_path}")
        else:
            logo_data = self._generate_product_logo(product_title)
            print(f"  Создано автоматическое изображение для продукта")
            
        files = {
            'logo': ('product_logo.png', BytesIO(logo_data), 'image/png')
        }
        
        response = self.session.patch(
            f"{API_BASE}/products/logo/{product_id}",
            files=files
        )
        response.raise_for_status()
        print(f"  ✓ Обновлен логотип продукта")
        return response.json()
    
    def _generate_product_logo(self, product_title):
        """Генерация изображения продукта"""
        colors = ['#2C3E50', '#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
        bg_color = random.choice(colors)
        
        img = Image.new('RGB', (600, 400), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Рисуем простую иконку кроссовка
        draw.ellipse([100, 150, 500, 350], fill='white', outline='black', width=3)
        draw.rectangle([150, 200, 450, 300], fill=bg_color)
        
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
        
    def create_size(self, product_id, size, count):
        """Создание размера для продукта"""
        data = {
            "product_id": product_id,
            "size": size,
            "count": count
        }
        
        response = self.session.post(
            f"{API_BASE}/sizes/",
            json=data
        )
        response.raise_for_status()
        size_obj = response.json()
        print(f"  ✓ Добавлен размер {size} (количество: {count})")
        return size_obj


def load_data_from_json(json_file):
    """Загрузка данных из JSON файла"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_template_json():
    """Создание шаблона JSON файла с данными"""
    data = {
        "brands": [
            {
                "name": "Nike",
                "logo_path": "images/brands/nike.png"  # Опционально
            },
            {
                "name": "Adidas",
                "logo_path": "images/brands/adidas.png"
            },
            {
                "name": "Puma",
                "logo_path": "images/brands/puma.png"
            },
            {
                "name": "Reebok",
                "logo_path": "images/brands/reebok.png"
            },
            {
                "name": "New Balance",
                "logo_path": "images/brands/new_balance.png"
            }
        ],
        "products": [
            {
                "brand_index": 0,
                "title": "Nike Air Max 270",
                "price": 12999,
                "color": "чёрный",
                "article": "AH8050-001",
                "category": "повседневные",
                "avg_grade": 4.5,
                "logo_path": "images/products/nike_air_max_270.png",
                "sizes": [
                    {"size": "42", "count": 10},
                    {"size": "43", "count": 15},
                    {"size": "44", "count": 8},
                    {"size": "45", "count": 5}
                ]
            },
            {
                "brand_index": 0,
                "title": "Nike ZoomX Vaporfly",
                "price": 21999,
                "color": "белый",
                "article": "AO4568-100",
                "category": "бег",
                "avg_grade": 4.8,
                "logo_path": "images/products/nike_vaporfly.png",
                "sizes": [
                    {"size": "40", "count": 7},
                    {"size": "41", "count": 12},
                    {"size": "42", "count": 10},
                    {"size": "43", "count": 6}
                ]
            },
            {
                "brand_index": 0,
                "title": "Nike LeBron 20",
                "price": 18999,
                "color": "красный",
                "article": "DJ5423-600",
                "category": "баскетбол",
                "avg_grade": 4.6,
                "logo_path": "images/products/nike_lebron_20.png",
                "sizes": [
                    {"size": "43", "count": 8},
                    {"size": "44", "count": 12},
                    {"size": "45", "count": 10}
                ]
            },
            {
                "brand_index": 1,
                "title": "Adidas Ultraboost 22",
                "price": 15999,
                "color": "синий",
                "article": "GZ0127",
                "category": "бег",
                "avg_grade": 4.7,
                "logo_path": "images/products/adidas_ultraboost.png",
                "sizes": [
                    {"size": "39", "count": 5},
                    {"size": "40", "count": 10},
                    {"size": "41", "count": 15},
                    {"size": "42", "count": 12}
                ]
            },
            {
                "brand_index": 1,
                "title": "Adidas Superstar",
                "price": 8999,
                "color": "белый",
                "article": "EG4958",
                "category": "повседневные",
                "avg_grade": 4.4,
                "logo_path": "images/products/adidas_superstar.png",
                "sizes": [
                    {"size": "40", "count": 20},
                    {"size": "41", "count": 18},
                    {"size": "42", "count": 15},
                    {"size": "43", "count": 10}
                ]
            },
            {
                "brand_index": 1,
                "title": "Adidas Dame 8",
                "price": 13999,
                "color": "зелёный",
                "article": "GZ2670",
                "category": "баскетбол",
                "avg_grade": 4.5,
                "logo_path": "images/products/adidas_dame.png",
                "sizes": [
                    {"size": "42", "count": 8},
                    {"size": "43", "count": 10},
                    {"size": "44", "count": 7},
                    {"size": "45", "count": 5}
                ]
            },
            {
                "brand_index": 2,
                "title": "Puma Deviate Nitro 2",
                "price": 14999,
                "color": "оранжевый",
                "article": "376587-01",
                "category": "бег",
                "avg_grade": 4.6,
                "logo_path": "images/products/puma_deviate.png",
                "sizes": [
                    {"size": "40", "count": 12},
                    {"size": "41", "count": 15},
                    {"size": "42", "count": 10}
                ]
            },
            {
                "brand_index": 2,
                "title": "Puma Suede Classic",
                "price": 6999,
                "color": "чёрный",
                "article": "352634-77",
                "category": "повседневные",
                "avg_grade": 4.3,
                "logo_path": "images/products/puma_suede.png",
                "sizes": [
                    {"size": "39", "count": 8},
                    {"size": "40", "count": 15},
                    {"size": "41", "count": 20},
                    {"size": "42", "count": 15},
                    {"size": "43", "count": 10}
                ]
            },
            {
                "brand_index": 2,
                "title": "Puma Fusion Nitro",
                "price": 9999,
                "color": "жёлтый",
                "article": "194451-02",
                "category": "тренинг",
                "avg_grade": 4.4,
                "logo_path": "images/products/puma_fusion.png",
                "sizes": [
                    {"size": "41", "count": 10},
                    {"size": "42", "count": 12},
                    {"size": "43", "count": 8},
                    {"size": "44", "count": 6}
                ]
            },
            {
                "brand_index": 3,
                "title": "Reebok Nano X2",
                "price": 11999,
                "color": "голубой",
                "article": "GZ0127",
                "category": "тренинг",
                "avg_grade": 4.5,
                "logo_path": "images/products/reebok_nano.png",
                "sizes": [
                    {"size": "40", "count": 8},
                    {"size": "41", "count": 10},
                    {"size": "42", "count": 12},
                    {"size": "43", "count": 8}
                ]
            },
            {
                "brand_index": 3,
                "title": "Reebok Classic Leather",
                "price": 7999,
                "color": "белый",
                "article": "49799",
                "category": "повседневные",
                "avg_grade": 4.2,
                "logo_path": "images/products/reebok_classic.png",
                "sizes": [
                    {"size": "39", "count": 10},
                    {"size": "40", "count": 15},
                    {"size": "41", "count": 18},
                    {"size": "42", "count": 15}
                ]
            },
            {
                "brand_index": 4,
                "title": "New Balance 1080v12",
                "price": 16999,
                "color": "фиолетовый",
                "article": "M1080N12",
                "category": "бег",
                "avg_grade": 4.7,
                "logo_path": "images/products/nb_1080.png",
                "sizes": [
                    {"size": "41", "count": 12},
                    {"size": "42", "count": 15},
                    {"size": "43", "count": 10},
                    {"size": "44", "count": 8}
                ]
            },
            {
                "brand_index": 4,
                "title": "New Balance 574",
                "price": 8999,
                "color": "синий",
                "article": "ML574EVE",
                "category": "повседневные",
                "avg_grade": 4.3,
                "logo_path": "images/products/nb_574.png",
                "sizes": [
                    {"size": "40", "count": 12},
                    {"size": "41", "count": 15},
                    {"size": "42", "count": 18},
                    {"size": "43", "count": 12},
                    {"size": "44", "count": 8}
                ]
            },
            {
                "brand_index": 0,
                "title": "Nike Metcon 8",
                "price": 13499,
                "color": "чёрный",
                "article": "DN8121-001",
                "category": "тренинг",
                "avg_grade": 4.6,
                "logo_path": "images/products/nike_metcon.png",
                "sizes": [
                    {"size": "41", "count": 10},
                    {"size": "42", "count": 14},
                    {"size": "43", "count": 11},
                    {"size": "44", "count": 7}
                ]
            },
            {
                "brand_index": 1,
                "title": "Adidas Solarboost 4",
                "price": 14499,
                "color": "оранжевый",
                "article": "GY5177",
                "category": "бег",
                "avg_grade": 4.5,
                "logo_path": "images/products/adidas_solarboost.png",
                "sizes": [
                    {"size": "40", "count": 9},
                    {"size": "41", "count": 13},
                    {"size": "42", "count": 11},
                    {"size": "43", "count": 8}
                ]
            }
        ]
    }
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✓ Создан файл data.json с шаблоном данных")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Заполнение API данными')
    parser.add_argument('--create-template', action='store_true', 
                       help='Создать шаблон JSON файла')
    parser.add_argument('--json-file', default='data.json',
                       help='Путь к JSON файлу с данными (по умолчанию: data.json)')
    parser.add_argument('--base-url', default='http://localhost:8000',
                       help='Базовый URL API (по умолчанию: http://localhost:8000)')
    
    args = parser.parse_args()
    
    if args.create_template:
        save_template_json()
        print("\nТеперь вы можете:")
        print("1. Отредактировать data.json")
        print("2. Добавить изображения в папки images/brands/ и images/products/")
        print("3. Запустить скрипт без параметра --create-template для загрузки данных")
        return
    
    global BASE_URL, API_BASE
    BASE_URL = args.base_url
    API_BASE = f"{BASE_URL}/api/v1"
    
    client = APIClient()
    
    try:
        # Загружаем данные из JSON
        print(f"\n=== ЗАГРУЗКА ДАННЫХ ИЗ {args.json_file} ===")
        data = load_data_from_json(args.json_file)
        
        # 1. Авторизация
        print("\n=== АВТОРИЗАЦИЯ ===")
        client.login()
        
        # 2. Создание брендов
        print("\n=== СОЗДАНИЕ БРЕНДОВ ===")
        brands = []
        for brand_data in data['brands']:
            brand = client.create_brand(
                name=brand_data['name'],
                logo_path=brand_data.get('logo_path')
            )
            brands.append(brand)
        
        # 3. Создание продуктов
        print("\n=== СОЗДАНИЕ ПРОДУКТОВ ===")
        products = []
        for product_data in data['products']:
            brand_id = brands[product_data['brand_index']]['id']
            
            product = client.create_product(
                brand_id=brand_id,
                title=product_data['title'],
                price=product_data['price'],
                color=product_data['color'],
                article=product_data['article'],
                category=product_data['category'],
                avg_grade=product_data.get('avg_grade', 4.5)
            )
            products.append(product)
            
            # Обновляем логотип продукта
            if 'logo_path' in product_data:
                client.update_product_logo(
                    product['id'],
                    logo_path=product_data['logo_path'],
                    product_title=product_data['title']
                )
            
            # 4. Создание размеров
            print(f"  Добавление размеров для {product_data['title']}:")
            for size_data in product_data['sizes']:
                client.create_size(
                    product['id'],
                    size_data['size'],
                    size_data['count']
                )
        
        print("\n=== СТАТИСТИКА ===")
        print(f"Создано брендов: {len(brands)}")
        print(f"Создано продуктов: {len(products)}")
        
        total_sizes = sum(len(p['sizes']) for p in data['products'])
        print(f"Создано размеров: {total_sizes}")
        
        print("\n✓ Данные успешно загружены!")
        
    except FileNotFoundError:
        print(f"\n✗ Файл {args.json_file} не найден!")
        print("Запустите скрипт с параметром --create-template для создания шаблона")
    except requests.exceptions.HTTPError as e:
        print(f"\n✗ Ошибка HTTP: {e}")
        if hasattr(e, 'response'):
            print(f"Ответ сервера: {e.response.text}")
    except Exception as e:
        print(f"\n✗ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()