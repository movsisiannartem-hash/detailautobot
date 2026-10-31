from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

router = Router()


def get_price_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🧮 Рассчитать для своего авто", callback_data="menu:calculator")
            ],
            [
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="nav:main_menu")
            ]
        ]
    )


@router.message(F.text == "📋 Полный прайс")
@router.callback_query(F.data == "menu:price")
async def show_price(event: Message | CallbackQuery, state: FSMContext):
    """Экран 5: Полный прайс-лист на услуги детейлинга."""
    await state.clear()

    text = (
        "📋 <b>ПРАЙС-ЛИСТ НА УСЛУГИ APEX DETAIL</b>\n\n"
        "<b>✨ 1. Восстановительная полировка кузова:</b>\n"
        "• Малый / средний класс: от 18 000 ₽\n"
        "• Бизнес-класс / кроссоверы: от 22 000 ₽\n"
        "• Внедорожники / минивэны: от 25 000 ₽\n\n"
        "<b>🧼 2. Детейлинг-химчистка салона:</b>\n"
        "• Малый / средний класс: от 12 000 ₽\n"
        "• Бизнес-класс / кроссоверы: от 14 500 ₽\n"
        "• Внедорожники / минивэны: от 17 000 ₽\n\n"
        "<b>🛡 3. Защита керамикой (2 слоя 9H):</b>\n"
        "• Малый / средний класс: от 25 000 ₽\n"
        "• Бизнес-класс / кроссоверы: от 30 000 ₽\n"
        "• Внедорожники / минивэны: от 35 000 ₽\n\n"
        "<b>💎 4. Комплекс 'All Inclusive' (Полировка + Керамика + Химчистка):</b>\n"
        "• Малый / средний класс: от 45 000 ₽\n"
        "• Бизнес-класс / кроссоверы: от 54 000 ₽\n"
        "• Внедорожники / минивэны: от 63 000 ₽\n\n"
        "<b>🔧 Дополнительные услуги:</b>\n"
        "• Бронирование фар полиуретаном: от 6 000 ₽\n"
        "• Оклейка зоны риска (капот, бампер, крылья): от 45 000 ₽\n"
        "• Покрытие стекол «Антидождь»: от 3 500 ₽ <i>(в подарок при записи через бот!)</i>\n\n"
        "<i>Точная смета формируется после бесплатного осмотра авто мастером.</i>"
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text=text, parse_mode="HTML", reply_markup=get_price_kb())
        await event.answer()
    else:
        await event.answer(text=text, parse_mode="HTML", reply_markup=get_price_kb())
