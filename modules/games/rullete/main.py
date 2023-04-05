import random
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

async def rullete(message: types.Message):
    ment = message.from_user.get_mention(as_html=True)
    rand = random.choice([f"{ment} выжил!\nБольше не рискуй подумай о друзьях и близких!", f"{ment} погиб в игре русская рулетка", "Пистолет не сработал!\nВот и хорошо!"])
    await message.answer(f"{rand}", reply=message.message_id)

def register_rullete_handlers(dp: Dispatcher):
    dp.register_message_handler(rullete, Text('русская рулетка', ignore_case=True))