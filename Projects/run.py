import asyncio  # Импортируем модуль asyncio для работы с асинхронным кодом
from Bot.config import TOKEN  # Импортируем токен бота из конфигурационного файла
from aiogram import Bot, Dispatcher  # Импортируем классы Bot и Dispatcher из aiogram
from Bot.handlers import router  # Импортируем маршрутизатор (router) с обработчиками команд
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Bot import apshed  # Импортируем модуль с функциями отправки сообщений
from datetime import datetime

async def main():
    """Основная асинхронная функция для инициализации и запуска бота."""
    bot = Bot(token=TOKEN)  # Создаем экземпляр бота с указанным токеном
    dp = Dispatcher()  # Создаем экземпляр диспетчера для обработки сообщений и команд
    dp.include_router(router)  # Подключаем маршрутизатор с обработчиками к диспетчеру

    # Инициализация планировщика
    scheduler = AsyncIOScheduler()
    
    # Добавление задач в планировщик
    scheduler.add_job(
        apshed.send_message_intervalDay,
        trigger='interval',
        seconds=10,  
        start_date=datetime.now(),
        kwargs={'bot': bot}
    )
    
    scheduler.add_job(
        apshed.send_message_intervalHour,
        trigger='interval',
        hours=1,  # Запускаем раз в час
        kwargs={'bot': bot}
    )
    
    scheduler.start()  # Запускаем планировщик

    try:
        await dp.start_polling(bot)  # Запускаем опрос бота для получения обновлений
    finally:
        await bot.close()  # Закрываем бота при завершении работы

if __name__ == '__main__':
    try:
        asyncio.run(main())  # Запускаем основную асинхронную функцию
    except KeyboardInterrupt:
        print('Exit')  # Обработка прерывания программы (например, Ctrl+C)
