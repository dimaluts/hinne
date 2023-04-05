from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from settings.users import if_user
from database import db
from random import randint
from .table import mine_tbl


async def add_value_to_mins(user_id, stavka):
    user = db(user_id)
    mines = []
    mines.append(randint(1, 25))
    for i in range(1, 6):
        a = randint(1, 25)
        if a in mines:
            pass
        else:
            mines.append(a)

    new_mines = []

    for i in range(1, 26):
        if i in mines:
            new_mines.append('\'1|❓\',')
        else:
            new_mines.append('\'0|❓\',')

    result = ' '.join(new_mines)
    result = result + f' \'Отмена!\', {stavka}, \'1\', {user_id}'

    user.inset_value_to_table(f'{user_id} MINE', result)


async def create_mines_buttons(user_id):
    user = db(user_id)
    data = user.select_from_table(f'\'{user_id} MINE\'')[0]
    markup = InlineKeyboardMarkup(row_width=5)
    kb1 = InlineKeyboardButton(
        data[0].split('|')[1], callback_data=f'{user_id}|11|mine')
    kb2 = InlineKeyboardButton(
        data[1].split('|')[1], callback_data=f'{user_id}|21|mine')
    kb3 = InlineKeyboardButton(
        data[2].split('|')[1], callback_data=f'{user_id}|31|mine')
    kb4 = InlineKeyboardButton(
        data[3].split('|')[1], callback_data=f'{user_id}|41|mine')
    kb5 = InlineKeyboardButton(
        data[4].split('|')[1], callback_data=f'{user_id}|51|mine')
    kb6 = InlineKeyboardButton(
        data[5].split('|')[1], callback_data=f'{user_id}|12|mine')
    kb7 = InlineKeyboardButton(
        data[6].split('|')[1], callback_data=f'{user_id}|22|mine')
    kb8 = InlineKeyboardButton(
        data[7].split('|')[1], callback_data=f'{user_id}|32|mine')
    kb9 = InlineKeyboardButton(
        data[8].split('|')[1], callback_data=f'{user_id}|42|mine')
    kb10 = InlineKeyboardButton(
        data[9].split('|')[1], callback_data=f'{user_id}|52|mine')
    kb11 = InlineKeyboardButton(
        data[10].split('|')[1], callback_data=f'{user_id}|13|mine')
    kb12 = InlineKeyboardButton(
        data[11].split('|')[1], callback_data=f'{user_id}|23|mine')
    kb13 = InlineKeyboardButton(
        data[12].split('|')[1], callback_data=f'{user_id}|33|mine')
    kb14 = InlineKeyboardButton(
        data[13].split('|')[1], callback_data=f'{user_id}|43|mine')
    kb15 = InlineKeyboardButton(
        data[14].split('|')[1], callback_data=f'{user_id}|53|mine')
    kb16 = InlineKeyboardButton(
        data[15].split('|')[1], callback_data=f'{user_id}|14|mine')
    kb17 = InlineKeyboardButton(
        data[16].split('|')[1], callback_data=f'{user_id}|24|mine')
    kb18 = InlineKeyboardButton(
        data[17].split('|')[1], callback_data=f'{user_id}|34|mine')
    kb19 = InlineKeyboardButton(
        data[18].split('|')[1], callback_data=f'{user_id}|44|mine')
    kb20 = InlineKeyboardButton(
        data[19].split('|')[1], callback_data=f'{user_id}|54|mine')
    kb21 = InlineKeyboardButton(
        data[20].split('|')[1], callback_data=f'{user_id}|15|mine')
    kb22 = InlineKeyboardButton(
        data[21].split('|')[1], callback_data=f'{user_id}|25|mine')
    kb23 = InlineKeyboardButton(
        data[22].split('|')[1], callback_data=f'{user_id}|35|mine')
    kb24 = InlineKeyboardButton(
        data[23].split('|')[1], callback_data=f'{user_id}|45|mine')
    kb25 = InlineKeyboardButton(
        data[24].split('|')[1], callback_data=f'{user_id}|55|mine')

    markup.row(kb1, kb2, kb3, kb4, kb5)
    markup.row(kb6, kb7, kb8, kb9, kb10)
    markup.row(kb11, kb12, kb13, kb14, kb15)
    markup.row(kb16, kb17, kb18, kb19, kb20)
    markup.row(kb21, kb22, kb23, kb24, kb25)
    markup.add(InlineKeyboardButton(
        data[25], callback_data=f'{user_id}|otmena|mine'))
    return markup


async def mine(message: types.Message):
    user_id = message.from_user.id
    ment = message.from_user.get_mention(as_html=True)
    user = db(user_id)
    if if_user(user_id, message):
        txt = message.text.split(' ')
        data = user.select_data('users')
        if txt[0].lower() in ['бомбы']:
            if len(txt) == 2:
                try:
                    if int(txt[1]) >= 10:
                        try:
                            bb = user.select_from_table(f'\'{user_id} MINE\'')
                            await message.answer(ment+', у вас уже запущены бомбы!')
                            mark = await create_mines_buttons(user_id)
                            await message.answer(f'{ment}, вы начали игру в бомбы!\nДля начала игры выберите одно из закрытых полей\nСтавка: {bb[0][26]}', reply_markup=mark)
                            return
                        except:
                            if int(data[1]) >= int(txt[1]):
                                try:
                                    ab = int(txt[1]) + 1
                                    user.create_table(
                                        f'{user_id} MINE', mine_tbl)
                                    await add_value_to_mins(user_id, txt[1])
                                    user.minus_value(
                                        int(txt[1]), 'hin', 'users')
                                    a = await create_mines_buttons(user_id)
                                    await message.answer(f'{ment}, вы начали игру в бомбы!\nДля начала игры выберите одно из закрытых полей\nСтавка: {txt[1]}', reply_markup=a)
                                except:
                                    chislo = '{число}'
                                    await message.answer(f'{ment}, вы ввели не число!\n\nИспользование: <code>бомбы</code> {chislo}')
                            else:
                                await message.answer(ment + ', на вашем счету не достаточно хин!')
                    else:
                        await message.answer(f'{ment}, минимальная ставка 10 хин')
                except:
                    pass
            else:
                await message.answer(ment + ', неправильные аргументы!\n\nПример: <code>бомбы</code> {число}')


def register_mine_handler(dp: Dispatcher):
    dp.register_message_handler(mine, Text(
        startswith=['бомбы'], ignore_case=True))
