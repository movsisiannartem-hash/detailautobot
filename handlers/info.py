from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import (
    COMPANY_ADDRESS,
    COMPANY_WORK_HOURS,
    COMPANY_PHONE,
    COMPANY_CHANNEL,
)
from keyboards.common_kb import get_info_kb

router = Router()


@router.message(F.text == "📍 Адрес и время работы")
@router.callback_query(F.data == "menu:info")
async def show_info(event: Message | CallbackQuery, state: FSMContext):
    """Экран 4: Адрес и контактная информация."""
    await state.clear()

    text = (
        "📍 <b>Наш адрес и контакты:</b>\n\n"
        f"🏢 <b>Адрес:</b> {COMPANY_ADDRESS}\n"
        f"⏰ <b>Режим работы:</b> {COMPANY_WORK_HOURS}\n"
        f"📞 <b>Телефон:</b> <code>{COMPANY_PHONE}</code>\n\n"
        f"📢 <b>Наш канал с процессами работ:</b> {COMPANY_CHANNEL}\n\n"
        "<i>Приезжайте на бесплатный осмотр состояния ЛКП и подбор защитных составов!</i>"
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text=text, parse_mode="HTML", reply_markup=get_info_kb())
        await event.answer()
    else:
        await event.answer(text=text, parse_mode="HTML", reply_markup=get_info_kb())
