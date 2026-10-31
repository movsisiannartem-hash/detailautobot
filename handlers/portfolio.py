from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from config import ASSETS_DIR
from keyboards.common_kb import get_portfolio_case_kb, get_back_to_main_kb

router = Router()

CASES = [
    {
        "service_id": "polishing",
        "file_name": "case_polishing.jpg",
        "caption": (
            "🔥 <b>Кейс 1: Глубокая восстановительная полировка кузова</b>\n\n"
            "▫️ <b>Автомобиль:</b> BMW 5-series (Черный сапфир)\n"
            "▫️ <b>Проблема:</b> Сильная «паутинка» после моек, потеря блеска, затертости лака.\n"
            "▫️ <b>Результат:</b> Удалено 95% микродефектов, возвращен глубокий зеркальный цвет без голограмм.\n"
            "⏱ <b>Время работы:</b> 1.5 дня."
        ),
    },
    {
        "service_id": "dry_cleaning",
        "file_name": "case_dry_cleaning.jpg",
        "caption": (
            "🧼 <b>Кейс 2: Детейлинг-химчистка светлой кожи салона</b>\n\n"
            "▫️ <b>Автомобиль:</b> Mercedes-Benz E-Class\n"
            "▫️ <b>Проблема:</b> Въевшийся синий пигмент от джинсов, засаленность и блеск кожи.\n"
            "▫️ <b>Результат:</b> Бережное очищение пор кожи без повреждения защитного лака + консервация матовым кремом с UV-фильтром.\n"
            "⏱ <b>Время работы:</b> 1 день."
        ),
    },
    {
        "service_id": "ceramic",
        "file_name": "case_ceramic.jpg",
        "caption": (
            "🛡 <b>Кейс 3: Нанесение 2 слоев премиальной нанокерамики 9H</b>\n\n"
            "▫️ <b>Автомобиль:</b> Porsche Cayenne\n"
            "▫️ <b>Эффект:</b> Угол смачивания 110° — мощный гидрофоб, вода и грязь слетают на скорости, кузов реже пачкается и легко моется.\n"
            "⏱ <b>Срок службы покрытия:</b> до 24 месяцев."
        ),
    },
]


@router.message(F.text == "📸 Наши работы (До/После)")
@router.callback_query(F.data == "menu:portfolio")
async def show_portfolio(event: Message | CallbackQuery, state: FSMContext):
    """Экран 3: Демонстрация портфолио с фотографиями До/После."""
    await state.clear()

    intro_text = (
        "📸 <b>Примеры выполненных работ в Apex Detail (До / После)</b>\n\n"
        "Листайте примеры ниже. Понравился результат? Нажмите <b>«Хочу так же»</b> для быстрого расчета стоимости для вашего авто!"
    )

    if isinstance(event, CallbackQuery):
        await event.message.answer(intro_text, parse_mode="HTML")
        await event.answer()
    else:
        await event.answer(intro_text, parse_mode="HTML")

    bot = event.bot
    chat_id = event.message.chat.id if isinstance(event, CallbackQuery) else event.chat.id

    for case in CASES:
        image_path = ASSETS_DIR / case["file_name"]
        kb = get_portfolio_case_kb(case["service_id"])

        if image_path.exists():
            photo = FSInputFile(str(image_path))
            await bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=case["caption"],
                parse_mode="HTML",
                reply_markup=kb,
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=case["caption"],
                parse_mode="HTML",
                reply_markup=kb,
            )
