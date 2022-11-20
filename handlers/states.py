from aiogram.dispatcher.filters.state import State, StatesGroup


class BuyProduct(StatesGroup):
    number = State()

class AddProduct(StatesGroup):
    category = State()
    info = State()
    photo = State()
    data = State()
