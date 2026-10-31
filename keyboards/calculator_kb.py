from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import CAR_CLASSES, SERVICES, MASTER_USERNAME


def get_car_classes_kb() -> InlineKeyboardMarkup:
    """Шаг 1: Клавиатура выбора класса автомобиля."""
    buttons = []
    for key, data in CAR_CLASSES.items():
        buttons.append([InlineKeyboardButton(text=data["title"], callback_data=f"class:{key}")])
    buttons.append([InlineKeyboardButton(text="🔙 Главное меню", callback_data="nav:main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_services_kb() -> InlineKeyboardMarkup:
    """Шаг 2: Клавиатура выбора услуги."""
    buttons = []
    for key, data in SERVICES.items():
        buttons.append([InlineKeyboardButton(text=data["title"], callback_data=f"service:{key}")])
    buttons.append([InlineKeyboardButton(text="🔙 Изменить класс авто", callback_data="calc:back_to_class")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="nav:main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_calculation_result_inline_kb() -> InlineKeyboardMarkup:
    """Шаг 3: Инлайн-кнопки под расчетом."""
    buttons = [
        [
            InlineKeyboardButton(
                text="✍️ Написать мастеру в личку",
                url=f"https://t.me/{MASTER_USERNAME.replace('@', '')}"
            )
        ],
        [
            InlineKeyboardButton(text="🔄 Рассчитать другую услугу", callback_data="menu:calculator"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="nav:main_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_contact_request_reply_kb() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой быстрой отправки номера телефона."""
    keyboard = [
        [KeyboardButton(text="📲 Отправить номер телефона", request_contact=True)],
        [KeyboardButton(text="🏠 В главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
