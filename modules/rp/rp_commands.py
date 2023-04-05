from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

async def send_rp(message: types.Message, text):
    await message.answer(f'{message.from_user.get_mention(as_html=True)}, {text} {message.reply_to_message.from_user.get_mention(as_html=True)}')

async def viebat(message: types.Message):
    await send_rp(message, 'выебал(а)')

async def pyat(message: types.Message):
    await send_rp(message, 'дал(а) пять')

async def ispugat(message: types.Message):
    await send_rp(message, 'испугал(а)')

async def izvinitsya(message: types.Message):
    await send_rp(message, 'извинился(лась) перед')

async def iznasilovat(message: types.Message):
    await send_rp(message, 'изнасиловал(а)')

async def kus(message: types.Message):
    await send_rp(message, 'кусьнул(а)')

async def kastr(message: types.Message):
    await send_rp(message, 'кастрировал(а)')

async def liznut(message: types.Message):
    await send_rp(message, 'лизнул')

async def obnyat(message: types.Message):
    await send_rp(message, 'обнял(а)')

def register_rp_commands_handler(dp: Dispatcher):
    dp.register_message_handler(viebat, Text('выебать', ignore_case=True))
    dp.register_message_handler(pyat, Text('дать пять', ignore_case=True))
    dp.register_message_handler(ispugat, Text('испугать', ignore_case=True))
    dp.register_message_handler(izvinitsya, Text('извиниться', ignore_case=True))
    dp.register_message_handler(iznasilovat, Text('изнасиловать', ignore_case=True))
    dp.register_message_handler(kus, Text('кусь', ignore_case=True))
    dp.register_message_handler(kastr, Text('кастрировать', ignore_case=True))
    dp.register_message_handler(liznut, Text('лизнуть', ignore_case=True))
    dp.register_message_handler(obnyat, Text('обнять', ignore_case=True))
