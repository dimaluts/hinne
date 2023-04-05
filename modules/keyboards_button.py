from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from settings.users import if_user
from database import db

async def profile(message: types.Message):
    user_id = message.from_user.id

    if if_user(user_id, message):
        user = db(user_id)
        data = user.select_data('users')
        give_limit = data[6]
        give_max = data[8]
        kb = InlineKeyboardMarkup()
        if message.chat.type == 'private':
            kb.add(InlineKeyboardButton('Повысить лимит', callback_data=f'{user_id}|hinne|limit'))
        await message.answer(f'<b>Профиль</b>\n'
                             f'🆔: <code>{user_id}</code>\n'
                             f'💰 Баланс: {user.hin} хин\n'
                             f'📊 Уровень: {user.lvl} ({user.xp}/{user.next_xp})\n'
                             f'Лимит передачи: {give_limit}/{give_max} хин', reply=message.message_id, reply_markup=kb)


async def games(message: types.Message):
    await message.answer('Все доступные игры:\n'
                         '<code>Бомбы</code> {ставка}\n'
                         '<code>Хотлайн</code> {ставка}')


async def razrabotka(message: types.Message):
    await message.answer('В разработке!')


def register_button_handlers(dp: Dispatcher):
    dp.register_message_handler(games, Text(['🎮игры'], ignore_case=True))
    dp.register_message_handler(profile, Text(
        ['👤профиль', 'профиль', 'п', 'проф'], ignore_case=True))
    dp.register_message_handler(razrabotka, Text(
        ['хогвартс', 'команды', 'донат', 'чаты', 'кланы', 'помощь', 'язык'], ignore_case=True))
