from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import sys
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Добавляем путь к родительской директории для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Database.database import Database
from Bot.keyboards import keyboard, get_number
from Bot.status import Clients
from aiogram.fsm.context import FSMContext
from aiogram import types
from datetime import datetime, timedelta, timezone



db = Database()  # Создаем объект класса Database
router = Router()  # Создаем объект класса Router

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Функция обработки команды start.

    Выводит приветственное сообщение и создает Reply клавиатуру с кнопками.
    """
    await message.answer(f"🌟 Привет! Рады вас видеть! чтобы зарегистрироваться нажмите на кнопку 'Запись'", reply_markup=keyboard)

@router.message(F.text == 'Запись')
async def register(message: Message, state: FSMContext):
    """Функция регистрации.

    Вызывается при нажатии кнопки 'Запись' или написании текста 'Запись'.
    Устанавливает статус Clients.name и запрашивает имя пользователя.
    """    
    await state.set_state(Clients.name)
    await message.answer('😊 Введите ваше имя:')

@router.message(Clients.name)
async def register_name(message: Message, state: FSMContext):
    """Функция получения имени.

    Сохраняет введенное имя в состоянии и запрашивает номер телефона.
    Устанавливает новый статус Clients.NumberPhone и показывает клавиатуру с кнопкой для предоставления номера.
    """
    await state.update_data(name=message.text)
    await state.set_state(Clients.NumberPhone)
    await message.answer("📞 Теперь введите ваш номер телефона:", reply_markup=get_number)

@router.message(Clients.NumberPhone)
async def register_numberPhone(message: Message, state: FSMContext):
    """Функция получения номера телефона.

    Проверяет введенный текст на пустоту и корректность.
    Если текст можно преобразовать в положительное число, сохраняет номер и запрашивает адрес.
    Если нет — выводит сообщение об ошибке. 
    Также обрабатывает случай, когда пользователь нажимает кнопку 'предоставить номер'.
    """
    if message.text:
        if message.text.isdigit():  
            await state.update_data(numberPhone=message.text)
            await state.set_state(Clients.Address)  
            await message.answer("🏠 Отлично! Теперь введите ваш адрес:")
        else:
            await message.reply("🚫 Пожалуйста, введите корректный номер телефона (только цифры).")
    elif message.contact:
        # Если пользователь отправил контакт
        await state.update_data(numberPhone=message.contact.phone_number)
        await state.set_state(Clients.Address)  
        await message.answer("🏠 Отлично! Теперь введите ваш адрес:")
    else:
        await message.reply("❓ Пожалуйста, введите номер телефона.")

@router.message(Clients.Address)
async def register_Address(message: Message, state: FSMContext):
    """Функция получения адреса.

    Сохраняет введенный адрес и выводит все данные, которые ввел пользователь.
    Создает запрос на сохранение данных в базе данных и очищает статус для возможности повторной записи.
    """
    await state.update_data(Address=message.text)
    # Получаем данные из состояния
    data = await state.get_data()
    
    # Выводим информацию пользователю
    await message.answer(f'🎉 Ваши данные:\nИмя: {data["name"]}\nНомер: {data["numberPhone"]}\nАдрес: {data["Address"]}')
    
    # Сообщаем о успешной регистрации и возвращаем клавиатуру
    await message.answer(f"✅ Вы успешно прошли запись, теперь выберите дату!", reply_markup=keyboard)
    
    # Сохраняем данные в базе данных
    db.set_query(message.from_user.id, data["name"], data["numberPhone"], data["Address"])
    
    # Очищаем состояние для возможности повторной записи
    await state.clear()

@router.message(F.text == 'Информация')
async def get_information(message: Message):
    user_id = message.from_user.id
    user_info = db.get_query(int(user_id))

    if user_info is None:
        await message.answer(f"😔 Вы еще не зарегистрированы. Пожалуйста, не забудьте выбрать дату!")
    else:
        # Проходим по всем записям в user_info
        for record in user_info:
            name, phone, address, date = record  # Предполагаем, что каждая запись - это кортеж из 4 элементов
            
            await message.answer(
                f"Имя: {name}\n"
                f"Телефон: +{phone}\n"
                f"Адрес: {address}\n"
                f"Дата: {date}\n"
            )

@router.message(F.text == 'Доступные слоты')
async def show_available_slots(message: Message):
        slots = db.get_available_slots()
        if not slots:
            await message.answer("😕 К сожалению, нет доступных слотов.")
            return

        keyboard = InlineKeyboardMarkup(inline_keyboard=[])

        for slot in slots:
            keyboard.inline_keyboard.append(
                [InlineKeyboardButton(
                    text=slot['TimeSlots'].strftime('%d-%m-%Y %H:%M'),
                    callback_data=f"slot_{slot['id']}"
                )]
            )
        await message.answer(f"🕒 Пожалуйста, выберите удобное время:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith('slot_'))
async def handle_slot_selection(callback_query: types.CallbackQuery):
    slot_id = int(callback_query.data.split('_')[1])
    user_id = db.get_CurrentUser(callback_query.from_user.id)

    if db.book_slot(user_id[0], slot_id):
        await callback_query.message.answer(f"🎉 Слот успешно забронирован! Спасибо!")
    else:
        await callback_query.message.answer("🚫 Ошибка при бронировании. Слот мог быть занят.")
