from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import get_main_menu_inline_kb, get_main_menu_reply_kb

router = Router()

WELCOME_TEXT = (
    "👋 <b>Добро пожаловать в детейлинг-центр Apex Detail!</b>\n\n"
    "Мы профессионально восстанавливаем блеск кузова, защищаем лак бронепленкой "
    "и возвращаем салону состояние нового авто.\n\n"
    "Выберите интересующий раздел в меню ниже:"
)


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    """Экран 1: Приветствие при команде /start."""
    await state.clear()
    # Отправляем сообщение с инлайн-меню и активируем нижнюю клавиатуру
    await message.answer(
        text=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=get_main_menu_reply_kb()
    )
    await message.answer(
        text="👇 <b>Главное меню:</b>",
        parse_mode="HTML",
        reply_markup=get_main_menu_inline_kb()
    )


@router.callback_query(F.data == "nav:main_menu")
async def handle_callback_main_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню через инлайн-кнопку."""
    await state.clear()
    if callback.message:
        await callback.message.edit_text(
            text=WELCOME_TEXT,
            parse_mode="HTML",
            reply_markup=get_main_menu_inline_kb()
        )
    await callback.answer()


@router.message(F.text.in_(["🏠 В главное меню", "🏠 Главное меню"]))
async def handle_text_main_menu(message: Message, state: FSMContext):
    """Возврат в главное меню через текстовую кнопку."""
    await state.clear()
    await message.answer(
        text=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=get_main_menu_inline_kb()
    )
