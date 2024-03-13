from aiogram.dispatcher.filters.state import State, StatesGroup


class PostState(StatesGroup):
    image = State()
    text = State()
    buttons = State()
    confirm = State()