import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from aiogram import Bot
import aiofiles
from config import LEADS_FILE, ADMIN_ID

logger = logging.getLogger(__name__)


async def save_lead(lead_data: dict) -> None:
    """Сохранение данных заявки в локальный JSON-файл."""
    try:
        leads = []
        if LEADS_FILE.exists():
            async with aiofiles.open(LEADS_FILE, mode="r", encoding="utf-8") as f:
                content = await f.read()
                if content.strip():
                    leads = json.loads(content)

        leads.append(lead_data)

        async with aiofiles.open(LEADS_FILE, mode="w", encoding="utf-8") as f:
            await f.write(json.dumps(leads, ensure_ascii=False, indent=2))
        logger.info(f"Лид успешно сохранен в {LEADS_FILE}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении лида в файл: {e}")


async def notify_admin_about_lead(bot: Bot, lead_data: dict) -> bool:
    """Отправка уведомления администратору/мастеру в Telegram."""
    if not ADMIN_ID:
        logger.info("ADMIN_TELEGRAM_ID не задан. Уведомление в Telegram пропущено.")
        return False

    username_str = f"@{lead_data.get('username')}" if lead_data.get('username') else "не указан"
    text = (
        "🔥 <b>НОВАЯ ЗАЯВКА С КАЛЬКУЛЯТОРА!</b>\n\n"
        f"👤 <b>Клиент:</b> {lead_data.get('full_name')} ({username_str})\n"
        f"📱 <b>Телефон:</b> <code>{lead_data.get('phone')}</code>\n"
        f"🚘 <b>Класс авто:</b> {lead_data.get('car_class')}\n"
        f"🛠 <b>Услуга:</b> {lead_data.get('service')}\n"
        f"💰 <b>Расчет:</b> {lead_data.get('price')}\n"
        f"⏱ <b>Срок:</b> {lead_data.get('duration')}\n"
        f"🎁 <b>Подарок:</b> Антидождь на лобовое стекло (зафиксирован)\n\n"
        f"📅 <i>Дата: {lead_data.get('created_at')}</i>"
    )

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="HTML")
        logger.info(f"Уведомление о лиде успешно отправлено администратору {ADMIN_ID}")
        return True
    except Exception as e:
        logger.warning(
            f"Не удалось отправить уведомление администратору {ADMIN_ID}: {e}. "
            f"(Убедитесь, что администратор запустил бота командой /start)"
        )
        return False


async def register_new_lead(bot: Bot, user, phone: str, calc_data: dict) -> dict:
    """Регистрация нового лида: сохранение и уведомление."""
    lead = {
        "user_id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "phone": phone,
        "car_class": calc_data.get("car_name", "Не указан"),
        "service": calc_data.get("service_name", "Не указана"),
        "price": calc_data.get("formatted_price", "Не указана"),
        "duration": calc_data.get("duration", "Не указан"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    await save_lead(lead)
    await notify_admin_about_lead(bot, lead)
    return lead
