import asyncio
from random import randint


async def create_mine_table():
    mine = []
    for i in range(1, 26):
        mine.append(f'\'{i}\' BIGINT,')
    name = ' '.join(mine)
    name = name + ' stavka BIGINT'
    print(name)


async def add_value_to_mins():
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
            new_mines.append(1)
        else:
            new_mines.append(0)

    print(mines)
    print(list(new_mines))

asyncio.run(add_value_to_mins())
