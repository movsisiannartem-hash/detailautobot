import re
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import CalculatorStates
from config import CAR_CLASSES, SERVICES, calculate_price
from keyboards.calculator_kb import (
    get_car_classes_kb,
    get_services_kb,
    get_calculation_result_inline_kb,
    get_contact_request_reply_kb,
)
from keyboards.main_menu import get_main_menu_reply_kb
from services.lead_service import register_new_lead

router = Router()


@router.message(F.text == "🧮 Рассчитать стоимость")
@router.callback_query(F.data == "menu:calculator")
async def start_calculator(event: Message | CallbackQuery, state: FSMContext):
    """Экран 2. Шаг 1: Выбор класса автомобиля."""
    await state.clear()
    await state.set_state(CalculatorStates.waiting_for_car_class)

    text = "🚗 <b>К какому классу относится ваш автомобиль?</b>\n\nВыберите вариант из списка:"

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text=text, parse_mode="HTML", reply_markup=get_car_classes_kb())
        await event.answer()
    else:
        await event.answer(text=text, parse_mode="HTML", reply_markup=get_car_classes_kb())


@router.callback_query(F.data.startswith("portfolio:calc:"))
async def start_calculator_from_portfolio(callback: CallbackQuery, state: FSMContext):
    """Быстрый старт расчета из карточки портфолио с предвыбранной услугой."""
    service_key = callback.data.split(":")[-1]
    await state.clear()
    await state.update_data(preselected_service=service_key)
    await state.set_state(CalculatorStates.waiting_for_car_class)

    text = (
        f"🎯 Вы выбрали услугу: <b>{SERVICES.get(service_key, {}).get('title', '')}</b>\n\n"
        "🚗 <b>К какому классу относится ваш автомобиль?</b>"
    )
    await callback.message.answer(text=text, parse_mode="HTML", reply_markup=get_car_classes_kb())
    await callback.answer()


@router.callback_query(F.data == "calc:back_to_class")
async def back_to_car_classes(callback: CallbackQuery, state: FSMContext):
    """Возврат к шагу выбора класса автомобиля."""
    await state.set_state(CalculatorStates.waiting_for_car_class)
    text = "🚗 <b>К какому классу относится ваш автомобиль?</b>\n\nВыберите вариант из списка:"
    await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=get_car_classes_kb())
    await callback.answer()


@router.callback_query(CalculatorStates.waiting_for_car_class, F.data.startswith("class:"))
async def process_car_class(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Шаг 2: Обработка выбранного класса и переход к выбору услуги."""
    car_class_key = callback.data.split(":")[1]
    await state.update_data(car_class=car_class_key)

    state_data = await state.get_data()
    preselected_service = state_data.get("preselected_service")

    # Если услуга уже была предвыбрана из портфолио, сразу переходим к расчету
    if preselected_service and preselected_service in SERVICES:
        await state.update_data(service=preselected_service)
        await show_calculation_result(callback, state)
        return

    await state.set_state(CalculatorStates.waiting_for_service)
    car_name = CAR_CLASSES.get(car_class_key, {}).get("short_name", "")
    text = (
        f"Выбран класс: <b>{car_name}</b>\n\n"
        "🛠 <b>Какая услуга вас интересует?</b>"
    )
    await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=get_services_kb())
    await callback.answer()


@router.callback_query(CalculatorStates.waiting_for_service, F.data.startswith("service:"))
async def process_service_selection(callback: CallbackQuery, state: FSMContext):
    """Шаг 3: Обработка выбранной услуги и показ итогового расчета."""
    service_key = callback.data.split(":")[1]
    await state.update_data(service=service_key)
    await show_calculation_result(callback, state)


async def show_calculation_result(callback: CallbackQuery, state: FSMContext):
    """Отображение итогового расчета и захват контакта."""
    data = await state.get_data()
    car_class = data.get("car_class", "business")
    service = data.get("service", "polishing")

    calc_res = calculate_price(car_class, service)
    await state.update_data(calc_result=calc_res)
    await state.set_state(CalculatorStates.waiting_for_contact)

    result_text = (
        f"Ориентировочная стоимость для класса <b>\"{calc_res['car_name']}\"</b>:\n"
        f"Услуга: <b>{calc_res['service_name']}</b>\n"
        f"💰 <b>Итого: {calc_res['formatted_price']}</b>\n"
        f"⏱ <b>Время работы:</b> {calc_res['duration']}\n\n"
        "🎁 <b>При бронировании через Telegram дарим антидождь на лобовое стекло в подарок!</b>\n\n"
        "Оставьте ваш номер телефона, мастер свяжется в течение 10 минут и зафиксирует скидку:"
    )

    # Редактируем инлайн-сообщение
    await callback.message.edit_text(
        text=result_text,
        parse_mode="HTML",
        reply_markup=get_calculation_result_inline_kb()
    )

    # Отправляем сообщение с удобной Reply-кнопкой для мгновенной отправки номера в 1 тап
    await callback.message.answer(
        text="👇 Нажмите кнопку ниже, чтобы поделиться номером в 1 клик, или напишите его в чат:",
        reply_markup=get_contact_request_reply_kb()
    )
    await callback.answer()


@router.message(CalculatorStates.waiting_for_contact, F.contact)
async def process_contact_button(message: Message, state: FSMContext, bot: Bot):
    """Получение контакта через кнопку отправки номера телефона."""
    contact = message.contact
    phone = contact.phone_number
    if not phone.startswith("+"):
        phone = f"+{phone}"

    data = await state.get_data()
    calc_res = data.get("calc_result", {})

    await register_new_lead(
        bot=bot,
        user=message.from_user,
        phone=phone,
        calc_data=calc_res
    )
    await state.clear()

    thanks_text = (
        f"🎉 <b>Спасибо, {message.from_user.first_name}! Заявка принята!</b>\n\n"
        f"🎁 Подарок <b>«Антидождь на лобовое стекло»</b> и скидка зафиксированы за номером <code>{phone}</code>.\n\n"
        "👨‍🔧 Мастер свяжется с вами в течение 10 минут для уточнения деталей и бронирования удобного времени."
    )
    await message.answer(text=thanks_text, parse_mode="HTML", reply_markup=get_main_menu_reply_kb())


@router.message(CalculatorStates.waiting_for_contact, F.text)
async def process_contact_text(message: Message, state: FSMContext, bot: Bot):
    """Получение номера телефона текстом (если пользователь ввел вручную)."""
    text = message.text.strip()

    if text in ["🏠 В главное меню", "🏠 Главное меню"]:
        await state.clear()
        await message.answer("Переход в главное меню.", reply_markup=get_main_menu_reply_kb())
        return

    # Простая валидация номера телефона (содержит минимум 7 цифр)
    digits = re.sub(r"\D", "", text)
    if len(digits) < 7:
        await message.answer(
            "⚠️ Пожалуйста, отправьте корректный номер телефона через кнопку ниже или введите номер вручную (например, +7 999 123-45-67):",
            reply_markup=get_contact_request_reply_kb()
        )
        return

    data = await state.get_data()
    calc_res = data.get("calc_result", {})

    await register_new_lead(
        bot=bot,
        user=message.from_user,
        phone=text,
        calc_data=calc_res
    )
    await state.clear()

    thanks_text = (
        f"🎉 <b>Спасибо, {message.from_user.first_name}! Заявка принята!</b>\n\n"
        f"🎁 Подарок <b>«Антидождь на лобовое стекло»</b> и скидка зафиксированы за номером <code>{text}</code>.\n\n"
        "👨‍🔧 Мастер свяжется с вами в течение 10 минут для уточнения деталей и бронирования удобного времени."
    )
    await message.answer(text=thanks_text, parse_mode="HTML", reply_markup=get_main_menu_reply_kb())
