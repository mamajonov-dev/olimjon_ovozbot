from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from data.config import *
from keyboards.default.psotbuttons import *

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    if str(message.chat.id) in ADMINS:
        await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=send_postbutton())
