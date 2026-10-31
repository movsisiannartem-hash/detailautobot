from .start import router as start_router
from .calculator import router as calculator_router
from .portfolio import router as portfolio_router
from .info import router as info_router
from .price import router as price_router
from .consultation import router as consultation_router

__all__ = [
    "start_router",
    "calculator_router",
    "portfolio_router",
    "info_router",
    "price_router",
    "consultation_router",
]
