from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from config import MASTER_USERNAME, COMPANY_PHONE, ADMIN_ID
from states import ConsultationStates
from keyboards.common_kb import get_back_to_main_kb
from keyboards.main_menu import get_main_menu_reply_kb

router = Router()


def get_consultation_kb() -> InlineKeyboardMarkup:
    phone_clean = COMPANY_PHONE.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✍️ Написать мастеру в Telegram",
                    url=f"https://t.me/{MASTER_USERNAME.replace('@', '')}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"📞 Позвонить: {COMPANY_PHONE}",
                    url=f"tel:{phone_clean}"
                )
            ],
            [
                InlineKeyboardButton(text="✏️ Написать вопрос прямо в бот", callback_data="consult:ask")
            ],
            [
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="nav:main_menu")
            ]
        ]
    )


@router.message(F.text == "💬 Консультация мастера")
@router.callback_query(F.data == "menu:consultation")
async def show_consultation(event: Message | CallbackQuery, state: FSMContext):
    """Экран 6: Консультация мастера."""
    await state.clear()

    text = (
        "💬 <b>Консультация старшего мастера Apex Detail</b>\n\n"
        "У вас нестандартная задача (глубокие сколы, притертость, пятна на светлой коже) "
        "или хотите прислать фото дефекта для предварительной оценки?\n\n"
        "Выберите удобный способ связи:"
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text=text, parse_mode="HTML", reply_markup=get_consultation_kb())
        await event.answer()
    else:
        await event.answer(text=text, parse_mode="HTML", reply_markup=get_consultation_kb())


@router.callback_query(F.data == "consult:ask")
async def prompt_question(callback: CallbackQuery, state: FSMContext):
    """Предложение ввести вопрос в бот."""
    await state.set_state(ConsultationStates.waiting_for_question)
    text = (
        "✍️ <b>Напишите ваш вопрос</b> (марку автомобиля, что требуется сделать, или приложите контакты):\n\n"
        "Мастер ответит вам в течение рабочего дня."
    )
    await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=get_back_to_main_kb())
    await callback.answer()


@router.message(ConsultationStates.waiting_for_question, F.text)
async def process_question(message: Message, state: FSMContext, bot: Bot):
    """Обработка полученного вопроса от клиента."""
    question = message.text.strip()
    user = message.from_user
    username_str = f"@{user.username}" if user.username else "не указан"

    if ADMIN_ID:
        try:
            admin_msg = (
                "❓ <b>НОВЫЙ ВОПРОС МАСТЕРУ ИЗ БОТА!</b>\n\n"
                f"👤 <b>Клиент:</b> {user.full_name} ({username_str})\n"
                f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"
                f"💬 <b>Сообщение:</b>\n<i>{question}</i>"
            )
            await bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="HTML")
        except Exception:
            pass

    await state.clear()
    await message.answer(
        "✅ <b>Ваш вопрос передан мастеру!</b>\n\nМы свяжемся с вами в ближайшее время.",
        parse_mode="HTML",
        reply_markup=get_main_menu_reply_kb()
    )
