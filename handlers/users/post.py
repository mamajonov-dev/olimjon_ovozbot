from aiogram.types import Message, CallbackQuery
from filters.channel import *
import sqlite3
from aiogram.dispatcher import FSMContext
from data.config import CHANNELS, NUMBERCHANNELS
from loader import bot, dp
from utils.misc.subscription import *
# from keyboards.inline.subcription import check_button
from keyboards.default.usersbuttons import *
from keyboards.default.psotbuttons import *
from keyboards.inline.regionsbutton import *
from loader import dp
from states.poststates import OvozberishState
from database import getcaptcha



@dp.message_handler(content_types='contact', state=OvozberishState.telefon)
@dp.message_handler(state=OvozberishState.telefon)
async def gettelefon(message: Message, state: FSMContext):
    chatid = message.chat.id
    if message.text:
        if message.text == '⬅️ Orqaga':
            await message.answer('Bosh menu', reply_markup=userasosiymenubutton())
            await state.finish()
        else:
            text = message.text.split()
            if len(message.text.split()) > 1:
                await message.answer(text='Telefon nomeringizni yuboring. Pastdagi <b>"Telefon raqam jo\'natish"</b> tugmasini bosing!\n                                                                      ⬇️', reply_markup=telefonbutton())
                data = message.text.split('/start')[1].strip()
                button, table = data.split('_')
                await state.update_data({'table_name': table, 'button_name': button})
                await OvozberishState.telefon.set()
            elif len(message.text.split()) == 1:
                await message.answer('Bosh menu. Telefon raqami kiritishda xatolik! \nQayta urinib ko\'ring', reply_markup=userasosiymenubutton())
                await state.finish()
    else:

        phone = message.contact.phone_number

        database = sqlite3.connect('database.sqlite')
        cursor = database.cursor()
        cursor.execute(f'''UPDATE users SET phone = ? WHERE chatid = ?''',
                       (phone, chatid))
        database.commit()
        database.close()
        await bot.send_contact(chat_id=NUMBERCHANNELS, phone_number=phone, first_name=message.from_user.first_name)

        contact = message.contact.phone_number
        await state.update_data({'contact': contact})
        await message.answer(text='Rasmdagi yozuvni kiriting', reply_markup=backbutton())
        captchaid, image, value = getcaptcha()
        await state.update_data({'value': value})
        await message.answer_photo(photo=image)
        await OvozberishState.captcha.set()


@dp.message_handler(state=OvozberishState.captcha)
async def getcaptchastate(message: Message, state: FSMContext):
    chatid = message.chat.id

    if message.text == '⬅️ Orqaga' or message.text == '/start':
        await message.answer('Bosh menu', reply_markup=userasosiymenubutton())
        await state.finish()
    else:
        data = await state.get_data()
        value = data['value']
        contact = data['contact']
        if contact and value and value == message.text:
            userid = message.from_user.id
            table_name = data['table_name']
            button_name = data['button_name']

            channel = CHANNELS
            status = await check(user_id=message.from_user.id, channel=channel)
            channel = await bot.get_chat(channel)

            if status:
                database = sqlite3.connect('database.sqlite')
                cursor = database.cursor()
                cursor.execute(f'''SELECT user_id FROM {table_name} WHERE user_id = ? AND phone = ?''',
                               (userid, contact))
                user = cursor.fetchone()
                database.close()
                if not user:
                    database = sqlite3.connect('database.sqlite')
                    cursor = database.cursor()
                    # await call.answer(text='true', show_alert=True)
                    cursor.execute(f"""INSERT INTO {table_name}(user_id, phone) VALUES (?, ?)""", (userid, contact))
                    database.commit()
                    database.close()
                    database = sqlite3.connect('database.sqlite')
                    cursor = database.cursor()
                    cursor.execute(f'''SELECT button_number FROM {table_name} WHERE button_name = ?''', (button_name,))
                    btnnumber = cursor.fetchone()[0]
                    btnnumber += 1
                    database.commit()
                    database.close()
                    database = sqlite3.connect('database.sqlite')
                    cursor = database.cursor()
                    cursor.execute(f'''UPDATE {table_name} SET button_number = ? WHERE button_name = ?''',
                                   (btnnumber, button_name))
                    database.commit()
                    database.close()

                    database = sqlite3.connect('database.sqlite')
                    cursor = database.cursor()
                    cursor.execute(f'''SELECT button_name, button_number FROM {table_name}
                                    ''')
                    butoon_data = cursor.fetchall()
                    # print(butoon_data)
                    butoon_d = []
                    for b in butoon_data:

                        if b[0] == None:
                            pass
                        else:
                            butoon_d.append(b)
                    # btn = regionsbutton(butoon_d, table_name)
                    # await message.edit_reply_markup(reply_markup=btn)
                    database.commit()
                    database.close()
                    await message.answer('✅ <b>OVOZINGIZ QABUL QILINDI\nIshtirokingiz uchun tashakkur!</b>', reply_markup=userasosiymenubutton())
                    # await message.answer(f'Bot yaratuvchisi:\n<i>"Bagdad IT Academy" o\'quv markazi</i>\n\nHamkorlik uchun \n@NurmuhammadMamajonov\nTel: <a href="tel:998917871199">+998917871199</a>', parse_mode='html')
                else:
                    database.close()
                    await message.answer('Bu so\'rovnomaga  ovoz bergansiz!‼️', reply_markup=userasosiymenubutton())
            else:
                await message.answer(
                    text=f'Kanalga obuna bo\'lmagansiz. Ovoz berish uchun kanlaga a\'zo bo\'ling\n\n⬇️⬇️⬇️⬇️⬇️⬇️⬇️\n\n{CHANNELS}', reply_markup=userasosiymenubutton())
                await state.finish()
        else:
            await message.answer('Captcha noto\'g\'ri. Boshqattan urinib ko\'ring', reply_markup=userasosiymenubutton())
            await state.finish()
        await state.finish()

    # result += f"<b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"

# invite_link = await channel.export_invite_link()
# result += (f"<b>{channel.title}</b> kanaliga obuna bo'lmagansiz!\n\n"
#            f"<a href='{invite_link}'>Obuna bo'ling </a>")
