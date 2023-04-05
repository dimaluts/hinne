from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from settings.users import if_user

from settings.markup import bonus_markup


async def bonus(message: types.Message):
    user_id = message.from_user.id
    if if_user(user_id, message):
        await message.answer('Получить бонус!', reply_markup=bonus_markup(user_id))


def register_bonus_handler(dp: Dispatcher):
    dp.register_message_handler(bonus, Text(
        ['бонус', '🎁бонусы', 'бонусы'], ignore_case=True))
