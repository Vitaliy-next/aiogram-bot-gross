from aiogram.fsm.state import StatesGroup, State

class OrderContactFSM(StatesGroup):
    waiting_contact_phone = State()

