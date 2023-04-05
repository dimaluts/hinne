from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from settings.users import if_user
from database import db


async def give(message: types.Message):
    user_id = message.from_user.id
    chislo = '{число}'
    ment = message.from_user.get_mention(as_html=True)
    txt = message.text.split(' ')
    reply = message.reply_to_message
    if if_user(user_id, message):
        user = db(user_id)
        if txt[0].lower() in ['д', 'дать']:
            if reply:
                reply_id = reply.from_user.id
                reply_ment = reply.from_user.get_mention(as_html=True)
                if if_user(reply_id, message=message):
                    reply_user = db(reply_id)
                    if len(txt) == 2:
                        hin = int(user.hin)
                        try:
                            a = int(txt[1]) + 1
                            if int(txt[1]) >= 1:
                                if hin >= int(txt[1]):
                                    if user_id != reply_id:
                                        data = user.select_data('users')
                                        give_limit = data[6]
                                        give_max = data[8]
                                        if int(give_max) < int(txt[1]) or int(txt[1]) > int(give_limit):
                                            await message.answer(f'У вас кончился лимит, еще можно передать {give_limit}/{give_max} хин.\nОбновление лимита каждных 12 часов!')
                                        else:
                                            user.minus_value(
                                                int(txt[1]), 'give_limit', 'users')
                                            user.minus_value(
                                                int(txt[1]), 'hin', 'users')
                                            reply_user.plus_value(
                                                int(txt[1]), 'hin', 'users')
                                            await message.answer(f'{ment}, вы передали {txt[1]} хин пользователю {reply_ment}.')
                                    else:
                                        await message.answer(f'{ment}, вы не можете передать деньги себе!')
                                else:
                                    await message.answer(f'{ment}, у вас недостаточно денег на балансе!')
                            else:
                                await message.answer(f'{ment}, вы не можете передать меньше 1 хин.')
                        except:
                            await message.answer(f'{ment}, вы ввели не число!')
                    else:
                        await message.answer(f'{ment}, вы ввели не правильные аргументы.\n\nПример: <code>дать</code> {chislo}.')
            else:
                await message.answer(f'{ment}, нужно ответить на сообщение пользователя!')


def register_give_value_handlers(dp: Dispatcher):
    dp.register_message_handler(give, Text(
        startswith=['д', 'дать'], ignore_case=True))
