import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp
from data.config import *
from keyboards.default.psotbuttons import *
from keyboards.default.usersbuttons import *
from states.poststates import OvozberishState
import database
from utils.misc.subscription import *

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    status = await check(user_id=message.from_user.id, channel=CHANNELS)
    markup1 = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Bag'dodim news", url=f'https://t.me/bagdodim_news'))
    markup.add(InlineKeyboardButton(text="Bag'dod hayoti", url=f'https://t.me/BAGDODHAYOTI'))

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Bag'dodim news", url=f'https://t.me/bagdodim_news'))
    if not status:
        

        await message.answer(
            text=f'Kanalga obuna bo\'lmagansiz. Ovoz berish uchun kanlaga a\'zo bo\'ling\n\', reply_markup=markup1)
        await state.finish()
    else:
        fullname = message.from_user.full_name
        chatid = message.chat.id
        username  = message.from_user.username
        database.registeruser(fullname, chatid, username)
        is_bot = message.from_user.is_bot
        if is_bot == False:
            if len(message.text.split()) > 1:
                data = message.text.split('/start')[1].strip()
                button, table = data.split('_')
                item = database.chekctable(table)
                print(item)
                if not item:
                    item = (1,)
                if item[0] != 0:
                    await message.answer('Bu so\'rovnoma tugatildi!', reply_markup=userasosiymenubutton())
                    await state.finish()
                else:
                    db = sqlite3.connect('database.sqlite')
                    cursor = db.cursor()
                    cursor.execute(f'''SELECT user_id FROM {table} WHERE user_id = ?''', (chatid, ))
                    user = cursor.fetchone()
                    if not user:
                        await message.answer(text='Telefon nomeringizni yuboring. Pastdagi <b>"Telefon raqam jo\'natish"</b> tugmasini bosing!\n                                                                      ⬇️', reply_markup=telefonbutton())
                        await state.update_data({'table_name': table, 'button_name': button})
                        await OvozberishState.telefon.set()
                    else:
                        await message.answer('Bu so\'rovnomaga  ovoz bergansiz!‼️', reply_markup=userasosiymenubutton())
                        await state.finish()
            elif len(message.text.split()) == 1:
                if chatid == 659237008:
                    await message.answer('Commands: \n/ads - reklama tarqatish\n/contacts - nomerlar\n/users - foydalanuvchilar\n/user_post - ovoz berganlar.')
                if int(message.chat.id) in ADMINS:
                    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=send_postbutton())
                elif int(message.chat.id) == 975763554:
                    await message.answer(
                        f'Xush kelibsiz {message.from_user.full_name}. So\'rovnomaga ovoz berish uchun kanal orqali kiring\n⬇️⬇️⬇️⬇️⬇️⬇️⬇️\n\n', reply_markup=markup)
                else:
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton(text="Bag'dodim news", url=f'https://t.me/bagdodim_news'))

                    await message.answer(f'Xush kelibsiz {message.from_user.full_name}. So\'rovnomaga ovoz berish uchun kanal orqali kiring\n⬇️⬇️⬇️⬇️⬇️⬇️⬇️\n\n', reply_markup=markup)
        else:
            pass
