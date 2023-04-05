from aiogram import types, Dispatcher

from settings.markup import *

from aiogram.dispatcher.filters import Text

from database import db

from settings import new_user


async def new_users(message: types.Message):
    if message.text != '/start':
        user_id = message.from_user.id

        user = db(user_id)

        data = user.is_user()

        if data is False:
            user.new_user('users', new_user(user_id))



async def start(message: types.Message):
    user_id = message.from_user.id

    user = db(user_id)

    data = user.is_user()

    if data is False:
        user.new_user('users', new_user(user_id))

    if message.chat.type == 'private':
        kb = start_markup()
    else:
        kb = None
    await message.answer('Добро пожаловать!\n\n'
                         'Hinne - это виртуальная валюта. У нас можно играть в разные игры\n\n'
                         'Валюту можно передавать другим пользователям.\n\n'
                         'Запустив бот вы принимаете пользовательское соглашение на пользование ботом.', reply_markup=kb)

async def get_chat_id(message: types.Message):
    await message.answer(f'<code>{message.chat.id}</code>')

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(get_chat_id, Text(['чат айди', 'chat id']))
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(new_users)
