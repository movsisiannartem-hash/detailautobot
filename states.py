from aiogram.fsm.state import State, StatesGroup


class CalculatorStates(StatesGroup):
    """Состояния для пошагового калькулятора детейлинга."""
    waiting_for_car_class = State()
    waiting_for_service = State()
    waiting_for_contact = State()


class ConsultationStates(StatesGroup):
    """Состояние для отправки вопроса мастеру."""
    waiting_for_question = State()
