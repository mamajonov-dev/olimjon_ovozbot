from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def testbutton(buttons: list):
    markup = InlineKeyboardMarkup()
    for button in buttons:
        markup.add(InlineKeyboardButton(text=f'{button} ', callback_data=f'region_{button}'))
    return markup

def regionsbutton(buttons: list, tname):
    markup = InlineKeyboardMarkup()
    for button, number in buttons:
        markup.add(InlineKeyboardButton(text=f'{button} {number}', callback_data=f'region_{button}_{tname}'))
    return markup