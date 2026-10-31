import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Основные настройки бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_TELEGRAM_ID = os.getenv("ADMIN_TELEGRAM_ID", "")
try:
    ADMIN_ID = int(ADMIN_TELEGRAM_ID) if ADMIN_TELEGRAM_ID else None
except ValueError:
    ADMIN_ID = None

COMPANY_NAME = os.getenv("COMPANY_NAME", "Apex Detail")
COMPANY_PHONE = os.getenv("COMPANY_PHONE", "+7 (999) 000-00-00")
COMPANY_ADDRESS = os.getenv("COMPANY_ADDRESS", "г. Москва, ул. Примерная, 15 (бокс 4)")
COMPANY_WORK_HOURS = os.getenv("COMPANY_WORK_HOURS", "Ежедневно с 10:00 до 21:00 (по предварительной записи)")
COMPANY_CHANNEL = os.getenv("COMPANY_CHANNEL", "@channel")
YANDEX_MAPS_URL = os.getenv("YANDEX_MAPS_URL", "https://yandex.ru/maps/?text=Москва,+ул.+Примерная+15")
MASTER_USERNAME = os.getenv("MASTER_USERNAME", "apex_master")

# Каталог классов авто
CAR_CLASSES = {
    "small": {
        "id": "small",
        "title": "1. Малый/Средний класс (Polo, Solaris, 3-series)",
        "short_name": "Малый / Средний класс",
        "multiplier": 1.0,
    },
    "business": {
        "id": "business",
        "title": "2. Бизнес-класс / Кроссоверы (Camry, RAV4, X3)",
        "short_name": "Бизнес / Кроссовер",
        "multiplier": 1.2,
    },
    "suv": {
        "id": "suv",
        "title": "3. Большие внедорожники / Минивэны (LC 300, X7, V-class)",
        "short_name": "Внедорожник / Минивэн",
        "multiplier": 1.4,
    },
}

# Каталог услуг
SERVICES = {
    "polishing": {
        "id": "polishing",
        "title": "✨ Глубокая полировка кузова",
        "base_price": 18000,
        "duration": "1.5–2 дня",
        "description": "Восстановление глубокого глянца, удаление до 95% паутинки и царапин, финишная антиголограммная доводка.",
    },
    "dry_cleaning": {
        "id": "dry_cleaning",
        "title": "🧼 Детейлинг-химчистка салона",
        "base_price": 12000,
        "duration": "1 день",
        "description": "Глубокая бережная очистка кожи, алькантары, текстиля и пластика, обработка защитными кондиционерами и озонирование.",
    },
    "ceramic": {
        "id": "ceramic",
        "title": "🛡 Защита керамикой (2 слоя)",
        "base_price": 25000,
        "duration": "1–2 дня",
        "description": "Нанесение 2 слоев нанокерамического состава 9H. Экстремальный гидрофобный эффект, глубина цвета и защита от реагентов.",
    },
    "all_inclusive": {
        "id": "all_inclusive",
        "title": "💎 Полный комплекс 'All Inclusive'",
        "base_price": 45000,
        "duration": "2–3 дня",
        "description": "Восстановительная полировка + 2 слоя керамики + химчистка салона с консервацией + гидрофоб стекол 'Антидождь'.",
    },
}

# Путь для сохранения лидов
LEADS_FILE = BASE_DIR / "leads.json"
ASSETS_DIR = BASE_DIR / "assets" / "images"


def calculate_price(car_class_key: str, service_key: str) -> dict:
    """Расчет итоговой стоимости с округлением до красивой суммы."""
    car_info = CAR_CLASSES.get(car_class_key)
    service_info = SERVICES.get(service_key)

    if not car_info or not service_info:
        return {
            "price": 0,
            "formatted_price": "по запросу",
            "duration": "уточняйте у мастера",
            "car_name": "Не указан",
            "service_name": "Не указана",
        }

    raw_price = service_info["base_price"] * car_info["multiplier"]
    # Округление до ближайших 1000 руб
    rounded_price = int(round(raw_price / 1000.0) * 1000)

    # Форматирование с пробелом между разрядами (например, "22 000")
    formatted_price = f"{rounded_price:,}".replace(",", " ")

    return {
        "price": rounded_price,
        "formatted_price": f"от {formatted_price} руб.",
        "duration": service_info["duration"],
        "car_name": car_info["short_name"],
        "service_name": service_info["title"],
    }
