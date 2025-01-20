from aiogram.fsm.state import State, StatesGroup

class Clients(StatesGroup):
    """Класс Clients предназначен для хранения вводимых данных от пользователя.

    Параметры
    ----------
    name : State
        Сохраняет имя пользователя.
    NumberPhone : State
        Сохраняет номер телефона пользователя.
    Address : State
        Сохраняет адрес пользователя.
    """
    name = State()          # Состояние для ввода имени пользователя
    NumberPhone = State()   # Состояние для ввода номера телефона
    Address = State()       # Состояние для ввода адреса