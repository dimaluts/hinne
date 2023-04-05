from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings.users import if_user
from database import db

from random import randint


async def create_table(user_id, stavka):
    user = db(user_id)
    values = 'user_id BIGINT, v1 BIGINT, v2 BIGINT, stavka BIGINT'
    user.create_table(f'{user_id} HOT', values)
    rand = randint(0, 1)
    if rand == 1:
        v1 = 1
        v2 = 0
    elif rand == 0:
        v1 = 0
        v2 = 1

    user.inset_value_to_table(
        f'{user_id} HOT', f'{user_id}, {v1}, {v2}, {stavka}')


async def create_hotline_buttons(user_id, c1, c2, otmena):
    mk = InlineKeyboardMarkup()
    v1 = InlineKeyboardButton(c1, callback_data=f'{user_id}|v1|hot')
    v2 = InlineKeyboardButton(c2, callback_data=f'{user_id}|v2|hot')
    cancel = InlineKeyboardButton(
        otmena, callback_data=f'{user_id}|cancel|hot')
    mk.row(v1, v2).add(cancel)
    return mk

async def get_messages(message: types.Message):
    user_id = message.from_user.id
    ment = message.from_user.get_mention(as_html=True)
    user = db(user_id)
    if if_user(user_id, message):
        txt = message.text.split(' ')
        if txt[0].lower() in ['хот', 'хотлайн']:
            if len(txt) == 2:
                try:
                    bb = user.select_from_table(f'\'{user_id} HOT\'')
                    await message.answer(ment+', у вас уже запущены хотлайны!')
                    mk = await create_hotline_buttons(user_id, '⬜️', '⬜️', 'Отмена!')
                    await message.answer(f'{ment}, вы начали игру в хотлайн.', reply_markup=mk)
                    return 0
                except:
                    try:
                        a = int(txt[1]) + 1
                        data = user.select_data('users')
                        hin = data[1]
                        if int(txt[1]) >= 10:
                            if int(hin) >= int(txt[1]):
                                user.minus_value(int(txt[1]), 'hin', 'users')
                                await create_table(user_id, txt[1])
                                mk = await create_hotline_buttons(user_id, '⬜️', '⬜️', 'Отмена!')
                                await message.answer(f'{ment}, вы начали игру в хотлайн.', reply_markup=mk)
                            else:
                                await message.answer(f'{ment}, у вас недостаточно денег на балансе!')
                        else:
                            await message.answer(f'{ment}, минимальная ставка 10 хин.')
                    except:
                        chislo = '{число}'
                        await message.answer(f'{ment}, вы ввели не число!\n\nИспользование: <code>хотлайн</code> {chislo}')
            else:
                chislo = '{число}'
                await message.answer(f'{ment}, вы ввели неправильные аргументы!\n\nПример: <code>хотлайн</code> {chislo}.')


def register_hotline_handlers(dp: Dispatcher):
    dp.register_message_handler(get_messages, Text(
        startswith=['хотлайн', 'хот', 'лай'], ignore_case=True))
