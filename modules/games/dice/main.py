import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text


async def diice(message: types.Message):
    ment = message.from_user.get_mention(as_html=True)
    result = await message.answer_dice(reply=message.message_id)
    await asyncio.sleep(3)
    await message.answer(f'{ment} вам выпало {result.dice.value}', reply=result.message_id)


def register_dice_handlers(dp: Dispatcher):
    dp.register_message_handler(diice, Text('кубик', ignore_case=True))
