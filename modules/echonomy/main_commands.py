from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from settings.users import if_user
from database import db

async def main(message: types.Message):
    user_id = message.from_user.id
    if if_user(user_id, message):
        user = db(user_id)
        await message.answer(f'💰 Баланс: {user.hin} хин', reply=message.message_id)
        
def register_main_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(main, Text(['б', 'баланс', 'хин', 'хины'], ignore_case=True))
