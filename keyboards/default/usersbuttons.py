import sqlite3

from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def asosiymenubutoon():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    databse = sqlite3.connect('database.sqlite')
    cursor = databse.cursor()
    cursor.execute('''SELECT post_name FROM posts WHERE complete = 0''')
    post_names = cursor.fetchall()
    databse.close()
    for name in post_names:
        markup.add(
            KeyboardButton(text=f'📌 {name[0]}')
        )
    markup.add(
        KeyboardButton(text='⬅️ Orqaga')
    )
    return markup


def superadminasosiymenubutoon():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    databse = sqlite3.connect('database.sqlite')
    cursor = databse.cursor()
    cursor.execute('''SELECT post_name FROM posts''')
    post_names = cursor.fetchall()
    databse.close()
    for name in post_names:
        markup.add(
            KeyboardButton(text=f'📌 {name[0]}')
        )
    markup.add(
        KeyboardButton(text='⬅️ Orqaga')
    )
    return markup




def telefonbutton():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(text='Telefon raqam jo\'natish', request_contact=True),

    )
    markup.add(
        KeyboardButton(text='⬅️ Orqaga')
    )
    return markup


def userasosiymenubutton():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(text='🤝 Hamkorlik qilish'),
    )
    return markup