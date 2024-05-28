from aiogram.dispatcher.filters.state import State, StatesGroup


class PostState(StatesGroup):
    name = State()
    image = State()
    text = State()
    buttons = State()
    confirm = State()


class OvozberishState(StatesGroup):
    telefon = State()
    captcha = State()
    ovoz = State()

class SorovnomaStopState(StatesGroup):
    table = State()
    confirm = State()


