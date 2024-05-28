from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def backbutton():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(text='⬅️ Orqaga')
    )
    return markup

def confirmbutton():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(text='✅ Ha'),
        KeyboardButton(text='❌ Yo\'q')
    )
    return markup

def send_postbutton():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(text='📝 Post yaratish'),
        KeyboardButton(text='Savolnoma yaratish'),
        KeyboardButton(text='🚫 So\'rovnomani to\'xtatish'),
    )
    return markup


