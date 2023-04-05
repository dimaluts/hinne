from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from database import db
from settings.config import creator

class OrderAd(StatesGroup):
    waiting_for_text = State()
    geted_text = State()

async def start_ad(message: types.Message, state: FSMContext):
    if message.from_id in creator:
        kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))
        await message.answer('Введите текст рассылки!', reply_markup=kb)
        await state.set_state(OrderAd.waiting_for_text.state)
    else:
        await message.answer('Ты не создатель!')

async def get_text(message: types.Message, state: FSMContext):
    txt = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Да')
    b2 = KeyboardButton('Нет')
    kb.row(b1, b2)
    if txt != 'Отмена':
        await state.update_data(message_text=txt)
        await state.set_state(OrderAd.geted_text.state)
        await message.answer(f'{txt}')
        await message.answer(f'Все верно?', reply_markup=kb)
    else:
        await state.finish()
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())

async def check(message: types.Message, state: FSMContext):
    txt = message.text
    if txt == 'Да':
        user = db(message.from_id)
        all_users = user.select_from_table('users')
        all_chats = user.select_from_table('chats')
        user_data = await state.get_data()
        succed = 0
        fails = 0
        chat_succed = 0
        chat_fails = 0
        from main import send_logs
        for i in all_chats:
            try:
                await send_logs(i[0], user_data['message_text'])
                chat_succed += 1
            except:
                chat_fails =+ 1
        for i in all_users:
            try:
                await send_logs(i[0], user_data['message_text'])
                succed += 1
            except:
                fails =+ 1
        await message.answer(f'Завершена рассылка!\nУдачно: {succed}\nНеудачно: {fails}', reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Статистика по чатам!\nУдачно: {chat_succed}\nНеудачно: {chat_fails}')
        await state.finish()
    elif txt == 'Нет':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
    await state.finish()

def register_ad_handlers(dp: Dispatcher):
    dp.register_message_handler(start_ad, commands="send_ad", state="*")
    dp.register_message_handler(get_text, state=OrderAd.waiting_for_text)
    dp.register_message_handler(check, state=OrderAd.geted_text)