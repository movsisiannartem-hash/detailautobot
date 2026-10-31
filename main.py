import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import (
    start_router,
    calculator_router,
    portfolio_router,
    info_router,
    price_router,
    consultation_router,
)


async def set_main_commands(bot: Bot):
    """Установка списка команд в меню бота."""
    commands = [
        BotCommand(command="start", description="🏠 Главное меню"),
        BotCommand(command="calc", description="🧮 Рассчитать стоимость"),
        BotCommand(command="price", description="📋 Прайс-лист"),
        BotCommand(command="portfolio", description="📸 Наши работы (До/После)"),
        BotCommand(command="info", description="📍 Адрес и контакты"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)

    if not BOT_TOKEN or "YOUR_" in BOT_TOKEN:
        logger.error("КРИТИЧЕСКАЯ ОШИБКА: BOT_TOKEN не задан в .env файле!")
        sys.exit(1)

    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Подключение роутеров
    dp.include_router(start_router)
    dp.include_router(calculator_router)
    dp.include_router(portfolio_router)
    dp.include_router(price_router)
    dp.include_router(info_router)
    dp.include_router(consultation_router)

    # Установка подсказок в Telegram
    await set_main_commands(bot)

    # Сброс вебхуков и старых апдейтов перед запуском polling
    await bot.delete_webhook(drop_pending_updates=True)

    bot_info = await bot.get_me()
    logger.info(f"Бот @{bot_info.username} ({bot_info.first_name}) успешно запущен в режиме polling!")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Работа бота завершена.")
