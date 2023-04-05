from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from settings.users import if_user
from database import db
from settings.config import admins, creator, logs_chat


async def give(message: types.Message):
    user_id = message.from_user.id
    ment = message.from_user.get_mention(as_html=True)
    if user_id in admins:
        if message.reply_to_message:
            reply_id = message.reply_to_message.from_user.id
            if if_user(reply_id, message):
                user = db(reply_id)
                txt = message.text.split(' ')
                if len(txt) == 2:
                    from main import send_logs
                    try:
                        a = int(txt[1]) + 1
                        user.plus_value(int(txt[1]), 'hin', 'users')
                        await message.answer(f'{ment}, вы успешно выдали {txt[1]} хин пользователю {message.reply_to_message.from_user.get_mention(as_html=True)}.')
                        await send_logs(logs_chat, f'{ment} выдал {txt[1]} {message.reply_to_message.from_user.get_mention(as_html=True)} с id |<code>{message.reply_to_message.from_id}</code>|\n---------------------------------------')
                    except:
                        await message.answer(f'{ment}, вы ввели не число!')
    else:
        await message.answer(f'{ment}, вы не админ!')


async def give_back(message: types.Message):
    user_id = message.from_user.id
    ment = message.from_user.get_mention(as_html=True)
    if user_id in admins:
        if message.reply_to_message:
            reply_id = message.reply_to_message.from_user.id
            if if_user(reply_id, message):
                user = db(reply_id)
                txt = message.text.split(' ')
                if len(txt) == 2:
                    from main import send_logs
                    try:
                        a = int(txt[1]) + 1
                        user.minus_value(int(txt[1]), 'hin', 'users')
                        await message.answer(f'{ment}, вы успешно забрали {txt[1]} хин у пользователя {message.reply_to_message.from_user.get_mention(as_html=True)}.')
                        await send_logs(logs_chat, f'{ment} забрал {txt[1]} у {message.reply_to_message.from_user.get_mention(as_html=True)}')
                    except:
                        await message.answer(f'{ment}, вы ввели не число!')
    else:
        await message.answer(f'{ment}, вы не админ!')


async def give_by_id(message: types.Message):
    user_id = message.from_user.id
    ment = message.from_user.get_mention(as_html=True)
    if if_user(user_id, message):
        if user_id in creator:
            txt = message.text.split(' ')
            if len(txt) == 3 and txt[0] == 'give':
                user = db(int(txt[1]))
                if user.is_user():
                    try:
                        a = int(txt[1]) + 1
                        user.plus_value(int(txt[2]), 'hin', 'users')
                        await message.answer(f'{ment}, вы выдали {txt[2]} хин пользователю с айди <code>{txt[1]}</code>')

                    except:
                        await message.answer(f'{ment}, вы ввели не число!')
                else:
                    await message.answer(f'{ment}, пользователя под таким id не существует!')


async def obnul(message: types.Message):
    user_id = message.from_user.id
    ment = message.from_user.get_mention(as_html=True)
    if if_user(user_id, message):
        if user_id in creator:
            if message.reply_to_message:
                reply_id = message.reply_to_message.from_user.id
                if if_user(reply_id, message):
                    user = db(reply_id)
                    user.set_value('hin', 2500, 'users')
                    user.set_value('xp', 0, 'users')
                    user.set_value('lvl', 0, 'users')
                    user.set_value('next_xp',  100, 'users')
                    user.set_value('bonus_time', 0, 'users')
                    user.set_value('give_limit', 5000, 'users')
                    user.set_value('give_time', 0, 'users')
                    user.set_value('give_max', 5000, 'users')
                    await message.answer(f'{ment}, вы обнулили пользователя {message.reply_to_message.from_user.get_mention(as_html=True)}.')
            else:
                await message.answer(f'{ment}, вы не ответили на сообщение пользователя!')
        else:
            await message.answer(f'{ment}, вы не создатель бота!')


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(give, Text(
        startswith=['выдать'], ignore_case=True))
    dp.register_message_handler(give_back, Text(
        startswith=['забрать'], ignore_case=True))
    dp.register_message_handler(give_by_id, Text(
        startswith=['give'], ignore_case=True))
    dp.register_message_handler(obnul, Text('обнулить', ignore_case=True))
