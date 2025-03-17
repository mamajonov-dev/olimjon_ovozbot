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
from states.poststates import OvozberishState
from database import getcaptcha

@dp.callback_query_handler(lambda call: 'region' in call.data)
async def getregion(call: CallbackQuery):
    try:
        userid = call.from_user.id
        _, tname = call.data.split('_')
        print(call.data)

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
        btn = gotobotbutton(butoon_d, tname)
        await call.message.edit_reply_markup(reply_markup=btn)
        database.commit()
        database.close()
    except:
        pass