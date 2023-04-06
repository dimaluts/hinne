from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.types import ContentTypes

from settings.users import if_user
from database import db


async def balance(message: types.Message):
    if message.chat.type.lower() == 'supergroup':
        user_id = message.from_id
        if if_user(user_id, message):
            user = db(user_id)
            chat_balance = user.select_value_where('kazna', 'chat_id', message.chat.id, 'chats')
            await message.answer(f'Казна чата: {chat_balance}')
    else:
        await message.answer('Эта команда доступна только в группах!')


async def add_to_kazna(message: types.Message):
    if message.chat.type.lower() == 'supergroup':
        user_id = message.from_id
        txt = message.text
        ment = message.from_user.get_mention(as_html=True)
        if if_user(user_id, message):
            user = db(user_id)
            if len(txt.split(' ')) == 2:
                val = txt.split(' ')[1]
                hin = user.hin
                try:
                    a = 1+int(val)
                    if int(hin) >= int(val):
                        if int(val) <= 0:
                            await message.answer(f'Нельзя положить в казну меньше 1 хин!')
                        else:
                            user.minus_value(int(val), 'hin', 'users')
                            user.add_value_where('kazna', int(val), 'chat_id', message.chat.id, 'chats')
                            await message.answer(f'{ment}, вы положили в казну чата {val} хин!')
                    else:
                        await message.answer(f'{ment}, у вас недостаточно хин!')
                except:
                    await message.answer('Вы ввели не число!')
            else:
                await message.answer(f'Неправильные аргументы!\nПример: <code>+казна</code> {"{число}"}')
    else:
        await message.answer('Эта команда доступна только в группах!')


async def add_user(message: types.Message):
    if message.chat.type.lower() == 'supergroup':
        user_id = message.from_id
        ment = message.from_user.get_mention(as_html=True)
        ment_us = message.new_chat_members[0].get_mention(as_html=True)
        if if_user(user_id, message):
            user = db(user_id)
            chat_balance = user.select_value_where('kazna', 'chat_id', message.chat.id, 'chats')
            if chat_balance >= 500:
                user.minus_value_where('kazna', 500, 'chat_id', message.chat.id, 'chats')
                user.plus_value(500, 'hin', 'users')
                await message.answer(f'{ment}, вы додали пользователя {ment_us} и получили 500 хин на баланс!')


def register_kazna_handlers(dp: Dispatcher):
    dp.register_message_handler(add_to_kazna, Text(startswith='+казна', ignore_case=True))
    dp.register_message_handler(balance, Text('казна', ignore_case=True))
    dp.register_message_handler(add_user, content_types=ContentTypes.NEW_CHAT_MEMBERS)
