import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.menu import menuAdmin, menu
from loader import dp, db
import datetime

currentDateTime = datetime.datetime.now()
dttm = currentDateTime.strftime("%Y-%m-%d")


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    try:
        db.add_user(message.from_user.id, name, dttm, 0, "")

    except sqlite3.IntegrityError as er:
        print(er)

    userId = str(message.from_user.id)

    if userId in ADMINS:
        print("YES")
        await message.answer("\n".join([
            f'Привет , {message.from_user.full_name}!'

        ]), reply_markup=menuAdmin)

    else:
        print("NO")

        allusers = db.select_all_ausers()
        all_ausers = []
        for user in allusers:
            all_ausers.append(user[1])
        print(all_ausers)
        uds = str(message.from_user.id)
        print(uds)

        if uds in all_ausers:
            print("Your ID is in the records!")

            await message.answer("\n".join([
                f'Привет , {message.from_user.full_name}!',
                'Теперь ты можешь использовать этот бот !',

            ]), reply_markup=menu)
        else:
            print("Your ID is not in the records.")
            await message.answer("\n".join([
                f'Привет , {message.from_user.full_name}!',
                'Ты не можешь использовать этот бот !',
                'По вопросу использования напиши @tamtam!',

            ]))

        # await message.answer("\n".join([
        #     f'Привет , {message.from_user.full_name}!',
        #     'Теперь вы участвуете в накопительной программе ДОМ 27 !',
        #
        # ]), reply_markup=menu)
