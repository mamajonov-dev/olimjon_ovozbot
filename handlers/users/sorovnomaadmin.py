from aiogram.types import Message, CallbackQuery
from filters.channel import *
import sqlite3
from aiogram.dispatcher import FSMContext
from data.config import CHANNELS
from loader import bot, dp
from utils.misc.subscription import *
# from keyboards.inline.subcription import check_button
from keyboards.default.usersbuttons import *
from keyboards.default.psotbuttons import *
from keyboards.inline.regionsbutton import *
from loader import dp
from states.poststates import OvozberishState, SorovnomaStopState
from database import getcaptcha, stoptable
from data.config import ADMINS

@dp.message_handler(text="🚫 So'rovnomani to'xtatish")
async def getstop(message: Message):
    chatid = message.chat.id
    if chatid in ADMINS:
        await message.answer('Qaysi so\'rovnomani to\'xtatmoqchisiz?', reply_markup=asosiymenubutoon())
        await SorovnomaStopState.table.set()
@dp.message_handler(state=SorovnomaStopState.table)
async def gettablename(message: Message, state: FSMContext):

    chatid = message.chat.id
    if message.text == '⬅️ Orqaga' or message.text == '/start':
        await message.answer('Asosiy menu', reply_markup=send_postbutton())
        await state.finish()
    else:
        table = message.text.split('📌')[1].strip()
        await message.answer('Tasdiqlaysizmi?', reply_markup=confirmbutton())
        await state.update_data({'table_name': table})
        await SorovnomaStopState.confirm.set()

@dp.message_handler(state=SorovnomaStopState.confirm)
async def gettableconfirm(message: Message, state: FSMContext):
    chatid = message.chat.id
    if message.text =='✅ Ha':
        data  = await state.get_data()
        table = data['table_name']
        stoptable(table)
        await message.answer('✅ So\'rovnoma to\'xtatildi ', reply_markup=send_postbutton())
        await state.finish()
    elif message.text == '❌ Yo\'q':
        await message.answer('Asosiy menu', reply_markup=send_postbutton())
        await state.finish()

