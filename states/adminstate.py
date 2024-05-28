from aiogram.dispatcher.filters.state import State, StatesGroup


class AdsState(StatesGroup):
    image = State()
    post = State()
    confirm = State()

class UsersPostState(StatesGroup):
    postname = State()

