from aiogram.fsm.state import State, StatesGroup
#from aiogram.fsm.state import StatesGroup, State

class AdminLogin(StatesGroup):
    waiting_password = State()


class AdminSQL(StatesGroup):
    waiting_query = State()


class AdminMessage(StatesGroup):
    waiting_text = State()
    waiting_media = State()


class GetPhone(StatesGroup):
    waiting_for_phone = State()



class InformState(StatesGroup):
    password = State()
    text = State()

class StockState(StatesGroup):
    password = State()
    text = State()

class PriseState(StatesGroup):
    password = State()
    text = State()

class PodiiState(StatesGroup):
    password = State()
    text = State()

class ProductState(StatesGroup):
    password = State()
    text = State()

class NewproductState(StatesGroup):
    password = State()
    text = State()

class CodeState(StatesGroup):
    password = State()
    sql = State()


# class NewVideoState(StatesGroup):
#     password = State()
#     media = State()
