from aiogram import types, Dispatcher
from modules.hotline.hotline import create_hotline_buttons
from modules.mines.mines import create_mines_buttons
from settings.users import if_user
from database import db

import time

from random import randint


async def callback_q(call: types.CallbackQuery):
    user_id = call.from_user.id
    ment = call.from_user.get_mention(as_html=True)
    call_datas = call.data.split('|')
    if if_user(user_id, call.message):
        user = db(user_id)
        # bombs
        # ______________________________________________________________________
        if call_datas[2] == 'mine' and int(call_datas[0]) == user_id:
            if call_datas[1] != 'otmena':
                try:
                    data = user.select_value(
                        f'"{call_datas[1]}"', f'{user_id} MINE')[0]
                    if data.split('|')[0] == '0' and data.split('|')[1] == '❓':
                        data_us = user.select_data(f'\'{user_id} MINE\'')
                        zarobotok = float(data_us[27])
                        zarobotok = zarobotok + 0.24
                        user.set_value(
                            'win', f'\'{zarobotok}\'', f'\'{user_id} MINE\'')
                        user.set_value(
                            f'\'{call_datas[1]}\'', '\'0|✅\'', f'\'{user_id} MINE\'')
                        user.set_value(
                            f'\'zabrat\'', '\'Забрать!\'', f'\'{user_id} MINE\'')
                        mk = await create_mines_buttons(user_id)
                        await call.message.edit_text(f'{ment}, вы начали игру в бомбы!\nДля начала игры выберите одно из закрытых полей\nСтавка: {data_us[26]}\nВыигрыш: {zarobotok}x', reply_markup=mk)
                    elif data.split('|')[0] == '1':
                        user.set_value(
                            f'\'{call_datas[1]}\'', '\'1|💣\'', f'\'{user_id} MINE\'')
                        user.set_value(f'\'zabrat\'', '\'\'',
                                       f'\'{user_id} MINE\'')
                        mk = await create_mines_buttons(user_id)
                        user.delete_table(f'{user_id} MINE')
                        await call.message.edit_text('Вы проиграли!', reply_markup=mk)
                except:
                    pass

            elif call_datas[1] == 'otmena':
                try:
                    data = user.select_data(f'\'{user_id} MINE\'')
                    if data[25] == 'Отмена!':
                        await call.message.delete()
                        user.plus_value(data[26], 'hin', 'users')
                        user.delete_table(f'{user_id} MINE')
                    else:
                        zarobotokk = float(data[27])
                        stavka = int(data[26])
                        summa = stavka * zarobotokk

                        await call.message.edit_text(f'Вы выиграли {int(summa)}')
                        user.plus_value(int(summa), 'hin', 'users')
                        user.delete_table(f'{user_id} MINE')
                except:
                    pass

        # hotline
        # ______________________________________________________________________
        if int(call_datas[0]) == user_id and call_datas[2] == 'hot':
            data_us = user.select_data(f'\'{user_id} HOT\'')
            if call_datas[1] == 'v1' and data_us[1] == 1:
                kb = await create_hotline_buttons(user_id, '🟥', '⬜️', '')
                await call.message.edit_text(f'{ment}, вы проиграли!', reply_markup=kb)
                user.delete_table(f'{user_id} HOT')
            elif call_datas[1] == 'v2' and data_us[2] == 1:
                kb = await create_hotline_buttons(user_id, '⬜️', '🟥', '')
                user.delete_table(f'{user_id} HOT')
                await call.message.edit_text(f'{ment}, вы проиграли!', reply_markup=kb)
            else:
                if call_datas[1] == 'v1' and data_us[1] == 0:
                    kb = await create_hotline_buttons(user_id, '🟩', '⬜️', '')
                    user.plus_value(int(data_us[3]*1.5), 'hin', 'users')
                    user.delete_table(f'{user_id} HOT')
                    await call.message.edit_text(f'{ment}, вы выиграли 1.5x!\n{int(data_us[3]*1.5)} хин', reply_markup=kb)
                elif call_datas[1] == 'v2' and data_us[2] == 0:
                    kb = await create_hotline_buttons(user_id, '⬜️', '🟩', '')
                    user.plus_value(int(data_us[3]*1.5), 'hin', 'users')
                    user.delete_table(f'{user_id} HOT')
                    await call.message.edit_text(f'{ment}, вы выиграли 1.5x!\n{int(data_us[3]*1.5)} хин', reply_markup=kb)

            if call_datas[1] == 'cancel' and call_datas[2] == 'hot':
                user.plus_value(int(data_us[3]), 'hin', 'users')
                await call.message.delete()
                user.delete_table(f'{user_id} HOT')

        # bonus
        # ______________________________________________________________________
        if int(call_datas[0]) == user_id and call_datas[1] == 'bonus':
            hin = user.select_data('users')[1]
            if hin < 10:
                us_data = user.select_data('users')
                bonus_time = us_data[5]
                current_time = time.time()
                if current_time - bonus_time >= 86400:
                    user.set_value('bonus_time', current_time, 'users')
                    bonus = randint(300, 1100)
                    user.plus_value(bonus, 'hin', 'users')
                    await call.message.edit_text(f'{ment}, вы получили бонус в размере {bonus} хин!')
                else:
                    await call.message.edit_text(f'{ment}, бонус можно брать каждные 24 часа!')
            else:
                await call.message.edit_text(f'{ment}, вы не можете получить бонус если ваш баланс больше 10!')
                
        # up limit
        # ______________________________________________________________________
        if int(call_datas[0]) == user_id and call_datas[2] == 'limit':
            data = user.select_data('users')
            hin = int(data[1])
            give_max = int(data[8])
            if hin >= give_max:
                user.set_value('give_max', give_max+give_max, 'users')
                user.minus_value(give_max, 'hin', 'users')
                user.set_value('give_limit', give_max+give_max, 'users')
                await call.message.answer(f'Вы успешно повысили свой лимит!\nТеперь ваш лимит {give_max+give_max} хин.')
            else:
                await call.message.answer(f'У вас недостаточно денег на балансе, еще нужно {give_max-hin} хин.')
            
        


def register_callback_handler(dp: Dispatcher):
    dp.register_callback_query_handler(callback_q)
