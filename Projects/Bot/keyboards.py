from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Объявление переменной keyboard.
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Запись'),   # Кнопка для записи
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Доступные слоты')
        ]
    ],
    resize_keyboard=True,  # Автоматическая подстройка размера клавиатуры
    input_field_placeholder='Выберите нужную кнопку...'  # Подсказка в поле ввода
)

# Объявление переменной get_number.
get_number = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить номер', request_contact=True)]  # Кнопка для отправки контакта
    ],
    resize_keyboard=True  # Автоматическая подстройка размера клавиатуры
)
