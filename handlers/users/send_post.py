from aiogram.types import Message
from aiogram.dispatcher import FSMContext
import sqlite3
from loader import *
from keyboards.inline.regionsbutton import *
from states.poststates import *
from data.config import CHANNELS
from keyboards.default.psotbuttons import *
from database import createposttable
from data.config import ADMINS


@dp.message_handler(text='📝 Post yaratish', )
async def getpost(message: Message):
    for admin in ADMINS:
        chat_id = message.chat.id
        if admin == chat_id:
            await message.answer('Post nomini kiritng ', reply_markup=backbutton())
            await PostState.name.set()


@dp.message_handler(state=PostState.name)
async def getname(message: Message, state: FSMContext):
    chatid = message.chat.id
    name = message.text
    if message.text == '⬅️ Orqaga' or message.text == '/start':
        await message.answer('Bosh menu', reply_markup=send_postbutton())
        await state.finish()
    else:
        database = sqlite3.connect('database.sqlite')
        cursor = database.cursor()

        cursor.execute('''SELECT post_name FROM posts WHERE post_name = ?''', (name,))
        post_name = cursor.fetchone()
        if not post_name:

            await state.update_data({'name': name})
            await message.answer(text='Faqat bitta rasm kiriting', reply_markup=backbutton())
            await PostState.image.set()
        else:
            await message.answer('Bu nom mavjud. Boshqa nom yozing')

@dp.message_handler(content_types=['photo'], state=PostState.image)
async def getimage(message: Message, state: FSMContext):
    image = message.photo[0]
    await message.answer('Post textini kiritng', reply_markup=backbutton())
    await state.update_data({'image': image.file_id})
    await PostState.text.set()


@dp.message_handler(state=PostState.text)
async def gettext(message: Message, state: FSMContext):
    text = message.text
    if text == '⬅️ Orqaga' or text == '/start':
        await message.answer('Bosh menu', reply_markup=send_postbutton())
        await state.finish()
    else:
        await state.update_data({'post': text})
        await message.answer('Knopkalarni enter bilan kiriting: masalan: \nOlma\ngilos\nanor\nnok',
                             reply_markup=backbutton())
        await PostState.buttons.set()


@dp.message_handler(state=PostState.buttons)
async def getbuttons(message: Message, state: FSMContext):
    text = message.text
    if text == '/start':
        await message.answer('Bosh menu', reply_markup=send_postbutton())
        await state.finish()
    elif text == '⬅️ Orqaga':
        await message.answer('Post textini kiritng', reply_markup=backbutton())
        await PostState.text.set()
    else:
        text = text.split('\n')
        buttons = testbutton(text)
        data = await state.get_data()
        post = data['post']
        image = data['image']
        posts = f'{post}'
        await state.update_data({'buttons': text})
        await message.answer_photo(photo=image, caption=posts, reply_markup=buttons)
        await message.answer('Tasdiqlaysizmi? ', reply_markup=confirmbutton())
        await PostState.confirm.set()


@dp.message_handler(state=PostState.confirm)
async def getcofirm(message: Message, state: FSMContext):
    text = message.text
    messageid = message.message_id
    messageid2 = message.message_id
    messageid = f't{messageid}'
    if text == '✅ Ha':
        data = await state.get_data()
        name = data['name']
        database = sqlite3.connect('database.sqlite')
        cursor = database.cursor()

        cursor.execute(f'''INSERT INTO posts (post_name)
                            VALUES (?)''', (name,))
        database.commit()
        database.close()

        post = data['post']
        image = data['image']
        buttons = data['buttons']
        createposttable(name)
        database = sqlite3.connect('database.sqlite')
        cursor = database.cursor()
        for button in buttons:
            cursor.execute(f'''INSERT INTO {name} (button_name)
                    VALUES (?)
                    ''', (button,))
            database.commit()
        database.close()
        database = sqlite3.connect('database.sqlite')
        cursor = database.cursor()
        cursor.execute(f'''SELECT button_name, button_number FROM {name}
        ''')
        butoon_data = cursor.fetchall()
        print(butoon_data)
        btn = gotobotbutton(butoon_data, name)
        # btn = regionsbutton(butoon_data, messageid)
        posttext = f'{post}'
        await bot.send_photo(chat_id=CHANNELS, photo=image, caption=posttext, reply_markup=btn)
        await message.answer('Post jo\'natildi', reply_markup=send_postbutton())
        await state.finish()
        database.commit()
        database.close()
    elif text == '❌ Yo\'q':
        await message.answer('Bosh menu', reply_markup=send_postbutton())
        await state.finish()
