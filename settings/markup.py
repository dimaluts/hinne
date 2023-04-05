from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
def start_markup():
    kb_button1 = KeyboardButton('👤Профиль')
    kb_button2 = KeyboardButton('Хогвартс')
    kb_button3 = KeyboardButton('Команды')
    kb_button4 = KeyboardButton('Донат')

    kb_button5 = KeyboardButton('Чаты')
    kb_button6 = KeyboardButton('Кланы')
    kb_button7 = KeyboardButton('🎮Игры')
    kb_button8 = KeyboardButton('🎁Бонусы')

    kb_button9 = KeyboardButton('Помощь')
    kb_button10 = KeyboardButton('Язык')
    kb = ReplyKeyboardMarkup()
    kb.row(kb_button1, kb_button2)
    kb.row(kb_button3, kb_button4)
    kb.row(kb_button5, kb_button6)
    kb.row(kb_button7, kb_button8)
    kb.row(kb_button9, kb_button10)

    return kb

def bonus_markup(user_id):
    kb = InlineKeyboardMarkup()
    bonus_b = InlineKeyboardButton('🎁', callback_data=f'{user_id}|bonus|bonus')
    kb.add(bonus_b)
    return kb
