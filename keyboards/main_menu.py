from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_inline_kb() -> InlineKeyboardMarkup:
    """Инлайн-клавиатура главного меню."""
    keyboard = [
        [
            InlineKeyboardButton(text="🧮 Рассчитать стоимость", callback_data="menu:calculator")
        ],
        [
            InlineKeyboardButton(text="📸 Наши работы (До/После)", callback_data="menu:portfolio")
        ],
        [
            InlineKeyboardButton(text="📋 Полный прайс", callback_data="menu:price")
        ],
        [
            InlineKeyboardButton(text="📍 Адрес и время работы", callback_data="menu:info")
        ],
        [
            InlineKeyboardButton(text="💬 Консультация мастера", callback_data="menu:consultation")
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_main_menu_reply_kb() -> ReplyKeyboardMarkup:
    """Постоянная нижняя клавиатура для быстрого доступа."""
    keyboard = [
        [KeyboardButton(text="🧮 Рассчитать стоимость")],
        [KeyboardButton(text="📸 Наши работы (До/После)"), KeyboardButton(text="📋 Полный прайс")],
        [KeyboardButton(text="📍 Адрес и время работы"), KeyboardButton(text="💬 Консультация мастера")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
