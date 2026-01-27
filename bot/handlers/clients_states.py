from aiogram.fsm.state import StatesGroup, State


class ClientsAccess(StatesGroup):
    waiting_password = State()


