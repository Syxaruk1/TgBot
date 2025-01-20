from aiogram import Bot
from Database.database import Database
from datetime import datetime, timedelta

# Инициализация базы данных
db = Database()
userData = db.get_All_register_user()

async def send_message(bot: Bot, user_id: int, address: str, message: str):
    """Отправка сообщения пользователю."""
    try:
        await bot.send_message(user_id, message.format(address=address))
    except Exception as e:
        print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

async def send_message_intervalDay(bot: Bot):
    """Проверка замеров на следующий день и отправка уведомлений."""
    target_date = datetime.now().date() + timedelta(days=1)
    for user_id, date_time, address in userData:
        if date_time.date() == target_date:
            await send_message(
                bot,
                user_id,
                address,
                "📢 Напоминаем, завтра замер по адресу: {address}."
            )

async def send_message_intervalHour(bot: Bot):
    """Проверка замеров через час и отправка уведомлений."""
    target_time = datetime.now() + timedelta(hours=1)
    for user_id, date_time, address in userData:
        # Проверяем совпадение даты и часа
        if (date_time.date() == target_time.date() and 
            date_time.hour == target_time.hour):
            await send_message(
                bot,
                user_id,
                address,
                "📢 Напоминаем, через час замер по адресу: {address}."
            )
