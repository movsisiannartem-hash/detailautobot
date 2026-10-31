from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import YANDEX_MAPS_URL, MASTER_USERNAME, COMPANY_CHANNEL


def get_info_kb() -> InlineKeyboardMarkup:
    """Клавиатура для экрана контактов и адреса."""
    buttons = [
        [
            InlineKeyboardButton(text="🗺 Открыть на Яндекс.Картах", url=YANDEX_MAPS_URL)
        ],
        [
            InlineKeyboardButton(text="📢 Наш Telegram-канал", url=f"https://t.me/{COMPANY_CHANNEL.replace('@', '')}")
        ],
        [
            InlineKeyboardButton(text="✍️ Написать мастеру", url=f"https://t.me/{MASTER_USERNAME.replace('@', '')}")
        ],
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="nav:main_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_portfolio_case_kb(service_id: str) -> InlineKeyboardMarkup:
    """Кнопка под кейсом До/После для перехода к расчету конкретной услуги."""
    buttons = [
        [
            InlineKeyboardButton(
                text="✨ Хочу так же — Рассчитать стоимость",
                callback_data=f"portfolio:calc:{service_id}"
            )
        ],
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="nav:main_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_to_main_kb() -> InlineKeyboardMarkup:
    """Простая кнопка возврата в главное меню."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🏠 В главное меню", callback_data="nav:main_menu")]]
    )
