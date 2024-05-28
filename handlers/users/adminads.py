import asyncio

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
import sqlite3
from loader import *
from keyboards.inline.regionsbutton import *
from states.adminstate import *
from data.config import CHANNELS, TESTNUMBERCHANNELS, NUMBERCHANNELS
from keyboards.default.psotbuttons import *
from keyboards.default.usersbuttons import *
from database import createposttable, getusers
from data.config import ADMINS
from aiogram.utils.exceptions import BotBlocked

a = 659237008


@dp.message_handler(commands='ads')
async def getads(message: Message):
    if message.chat.id == 659237008:
        await bot.send_message(chat_id=659237008, text='Post rasmini tanlang', reply_markup=backbutton())
        await AdsState.image.set()


@dp.message_handler(content_types='photo', state=AdsState.image)
@dp.message_handler(state=AdsState.image)
async def getadsimage(message: Message, state: FSMContext):
    if message.text:
        if message.text == '/start' or message.text == '⬅️ Orqaga':
            await bot.send_message(chat_id=a, text='Asosiy menu', reply_markup=send_postbutton())
            await state.finish()
    else:
        image = message.photo[0].file_id
        await state.update_data({'image': image})
        await bot.send_message(chat_id=a, text='Post kiriting', reply_markup=backbutton())

        await AdsState.post.set()


@dp.message_handler(state=AdsState.post)
async def getadspost(message: Message, state: FSMContext):
    if message.text == '/start' or message.text == '⬅️ Orqaga':
        await bot.send_message(chat_id=a, text='Asosiy menu', reply_markup=send_postbutton())
        await state.finish()
    else:
        post = message.text
        await state.update_data({'post': post})
        await bot.send_message(chat_id=a, text='Tasdiqlaysizmi?', reply_markup=confirmbutton())
        await AdsState.confirm.set()


@dp.message_handler(state=AdsState.confirm)
async def getadsconfirm(message: Message, state: FSMContext):
    if message.text == '❌ Yo\'q':
        await bot.send_message(chat_id=a, text='Asosiy menu', reply_markup=send_postbutton())
        await state.finish()
    elif message.text == '✅ Ha':
        data = await state.get_data()
        post = data['post']
        image = data['image']
        users = getusers()
        print(users)
        for user in users:
            try:
                await bot.send_photo(chat_id=user[0], caption=post, photo=image)
            except BotBlocked:
                await asyncio.sleep(1)
        await bot.send_message(chat_id=a, text='Post jonatildi', reply_markup=send_postbutton())
        await state.finish()


@dp.message_handler(commands='contacts')
async def showcontakts(message: Message):
    chatid = message.chat.id

    if chatid == a:
        database = sqlite3.connect('database.sqlite')
        cursor = database.cursor()
        cursor.execute('''SELECT phone, fullname, chatid FROM users''')
        contacts = cursor.fetchall()
        for contact, fullname, chat_id in contacts:
            await bot.send_contact(chat_id=TESTNUMBERCHANNELS, phone_number=contact, first_name=fullname)

            # try:
            #     # user = await bot.get_chat(message.text)
            #     user = message.from_user
            #     profile_photos = await bot.get_user_profile_photos(chat_id)
            #     if profile_photos.total_count > 0:
            #         photo = profile_photos.photos[0][0]  # Get the first photo in the first array
            #         file_info = await bot.get_file(photo.file_id)
            #         await message.answer_photo(photo=file_info.file_id)
            #         # file_path = file_info.file_path
            #         # await bot.send_photo(chat_id=message.chat.id,
            #         #                      photo=f'https://api.telegram.org/file/bot{API_TOKEN}/{file_path}')
            #     else:
            #         await message.reply("This user has no profile photo.")
            # except Exception as e:
            #     await message.reply(f"An error occurred: {e}")


@dp.message_handler(commands='users')
async def showusers(message: Message):
    chatid = message.chat.id

    if chatid == a:
        database = sqlite3.connect('database.sqlite')
        cursor = database.cursor()
        cursor.execute('''SELECT id, phone, fullname, chatid, username FROM users''')
        contacts = cursor.fetchall()
        for userid, contact, fullname, chat_id, username in contacts:
            text = f'{userid}. {contact}\n{fullname} \n@{username}\n\n'
            await bot.send_message(chat_id=TESTNUMBERCHANNELS, text=text)
        await bot.send_message(chat_id=a, text=f'All users: {len(contacts)}')


@dp.message_handler(commands='user_post')
async def showpostuser(message: Message):
    chatid = message.chat.id
    if chatid == a:
        await bot.send_message(chat_id=a, text='Postni tanlang', reply_markup=superadminasosiymenubutoon())
        await UsersPostState.postname.set()

@dp.message_handler(state=UsersPostState.postname)
async def getpoststatename(message: Message, state: FSMContext):
    postname = message.text.split('📌 ')[1]
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    cursor.execute(f'''SELECT *  FROM {postname}''')
    users = cursor.fetchall()
    await bot.send_message(TESTNUMBERCHANNELS, text=f'📌📌📌📌📌📌📌{postname}📌📌📌📌📌📌📌📌📌')
    for i in users:
        await bot.send_message(chat_id=TESTNUMBERCHANNELS, text=i)
        if i[3]:
            try:
                u = await bot.get_chat(i[3])
                await bot.send_contact(TESTNUMBERCHANNELS, phone_number=i[4], first_name=u.first_name)
                # await message.answer(u)
            except:
                pass
    await state.finish()


@dp.message_handler(text='🤝 Hamkorlik qilish')
async def gethamkorlik(message: Message):
    text = (f'Bog\'lanish\n'
            f'Telefon: +998917871199\n@NurmuhammadMamajonov')
    await message.answer(text)