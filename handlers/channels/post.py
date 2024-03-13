from aiogram.types import Message, CallbackQuery
from filters.channel import *
import sqlite3
from loader import *
from filters.channel import *
from data.config import CHANNELS
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import CHANNELS
from loader import bot, dp
from utils.misc.subscription import *
# from keyboards.inline.subcription import check_button
from keyboards.inline.regionsbutton import *
from loader import dp
import re


@dp.callback_query_handler(lambda call: 'region' in call.data)
async def getregion(call: CallbackQuery):
    userid = call.from_user.id
    _, btnname, tname = call.data.split('_')
    channel = CHANNELS
    status = await check(user_id=call.from_user.id, channel=channel)
    channel = await bot.get_chat(channel)
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    if status:
        try:
            # await call.answer(text='true', show_alert=True)
            cursor.execute(f"""INSERT INTO {tname}(user_id) VALUES (?)""", (userid, ))
            database.commit()
            database.close()
            database = sqlite3.connect('database.sqlite')
            cursor = database.cursor()
            cursor.execute(f'''SELECT button_number FROM {tname} WHERE button_name = ?''', (btnname, ))
            btnnumber = cursor.fetchone()[0]
            btnnumber += 1
            database.commit()
            database.close()
            database = sqlite3.connect('database.sqlite')
            cursor = database.cursor()
            cursor.execute(f'''UPDATE {tname} SET button_number = ? WHERE button_name = ?''', (btnnumber, btnname))
            database.commit()
            database.close()

            database = sqlite3.connect('database.sqlite')
            cursor = database.cursor()
            cursor.execute(f'''SELECT button_name, button_number FROM {tname}
                    ''')
            butoon_data = cursor.fetchall()
            print(butoon_data)
            butoon_d = []
            for b in butoon_data:

                if b[0] == None:
                    pass
                else:
                    butoon_d.append(b)
            btn = regionsbutton(butoon_d, tname)
            await call.message.edit_reply_markup(reply_markup=btn)
            database.commit()
            database.close()
            # result += f"<b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        except:
            database.close()
            await call.answer('Siz ovoz bergansiz!', show_alert=True)
    else:
        await call.answer(text='Kanalga obuna bo\'lmagansiz. Ovoz berish uchun kanlaga a\'zo bo\'ling', show_alert=True)

        # invite_link = await channel.export_invite_link()
        # result += (f"<b>{channel.title}</b> kanaliga obuna bo'lmagansiz!\n\n"
        #            f"<a href='{invite_link}'>Obuna bo'ling </a>")


