import asyncio
import csv
import time

from aiogram import types
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest, GetHistoryRequest
from telethon.tl.types import Channel, Chat, InputPeerEmpty, PeerChannel

from keyboards.default.menu import users
from loader import dp, bot, db

API_ID = '200469'
API_HASH = '5a7d00324871cbe0847cf9e061048a73'
phone = "+79997500005"

sent_messages = []


class FormPost(StatesGroup):
    post = State()


class FormChats(StatesGroup):
    chats = State()


class FormAusers(StatesGroup):
    ausers = State()


all_worlds = []


@dp.message_handler(text="Слова")
async def get_worlds(message: types.Message):
    print(message)
    await gets_worlds(message, 0)


@dp.callback_query_handler(lambda callback_query: True)
async def process_callback(callback_query: types.CallbackQuery):
    # Получаем переданный скрытый текст из callback_data кнопки
    callback_data = callback_query.data
    # print(callback_query.message.message_id)
    indef = callback_data.split('_')
    hidden_text = callback_data.split('_')[-1]  # Получаем скрытый текст из callback_data
    print(hidden_text)
    if indef[0] == "button":
        print("del worlds")
        await bot.answer_callback_query(callback_query.id, text=hidden_text)
        tgd = hidden_text

        db.delete_world(int(tgd))
        await callback_query.message.answer("Слово удалено и больше не доступен для парсинга")
        await gets_worlds(callback_query.message, 1)
    elif indef[0] == "buttons":
        print("dell chat")
        await bot.answer_callback_query(callback_query.id, text=hidden_text)
        tgd = hidden_text
        db.delete_chats(int(tgd))
        await callback_query.message.answer("Чат удален и больше не доступен для парсинга")
        await gets_chats(callback_query.message, 1)
    elif indef[0] == "auser":
        print(indef)
        tgd = hidden_text
        db.delete_ausers(int(tgd))
        await callback_query.message.answer("Пользователь удален ")
        await get_all_apr_users(callback_query.message, 1)


async def gets_worlds(message: types.Message, mode: int):
    if mode == 0:
        w_w = db.select_all_worlds()
        if len(w_w) == 0:
            await message.answer("Нет слов , для работы бота добавьте хотя бы одно ")
        for ww in w_w:
            # all_worlds.append(ww[1])
            # await message.answer(ww[1])

            keyboard = InlineKeyboardMarkup()
            # Передаем скрытый текст через параметр callback_data кнопки
            button_text = "Delete"
            message_id = message.message_id
            hidden_text = ww[0]
            callback_data = f"button_{button_text.replace(' ', '_')}_{hidden_text}"  # Форматирование строки для уникального callback_data
            button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
            keyboard.add(button)
            await message.answer(ww[1], reply_markup=keyboard)
    elif mode == 1:
        w_w_s = db.select_all_worlds()
        await message.answer("Измененный список слов")
        for ww in w_w_s:
            # all_worlds.append(ww[1])
            await message.answer(ww[1])


@dp.message_handler(text="Добавить слово")
async def get_change_worlds(message: types.Message):
    print(message)

    await FormPost.post.set()

    await message.answer("Напишите ключевое слово и отправьте его боту")


@dp.message_handler(state=FormPost.post, content_types=['text'])
async def process_name(message: types.Message, state: FormPost.post):
    async with state.proxy() as data:
        if message.content_type == 'photo':
            data['text'] = message.caption
        else:
            data['text'] = message.text
    await state.finish()
    print(f"{data['text']}")
    wld = f"{data['text']}"
    db.add_worlds(None, wld)
    # await FormPost.post.set()


@dp.message_handler(text="Проверить посты")
async def get_check_post(message: types.Message):
    client = TelegramClient("mibotdd", API_ID, API_HASH, system_version='4.16.30-vxCUSTOM')
    await client.start()

    dialogs = client.iter_dialogs()
    wlds = db.select_all_worlds()
    wlds_all = []
    for wld in wlds:
        wlds_all.append(wld[1])
    chats = db.select_all_chats()
    all_chats = []
    for chat in chats:
        all_chats.append(chat[1])

    async for dialog in dialogs:
        # print(dialog.title)
        founds = any(word in dialog.title for word in all_chats)
        # print(founds)
        if founds:
            print(dialog.title)
            part_mes = await client.get_messages(dialog.id, limit=10)
            for mss in part_mes:
                time.sleep(1)
                print(mss.text)
                if mss.text != '':
                    found = any(word in mss.text for word in wlds_all)
                    if found:
                        user = await client.get_entity(mss.sender_id)
                        await message.answer(mss.text,
                                             reply_markup=types.InlineKeyboardMarkup(
                                                 inline_keyboard=[
                                                     [
                                                         types.InlineKeyboardButton(text="Open Profile",
                                                                                    url=f"https://t.me/{user.username}")
                                                     ]
                                                 ]
                                             ))
    await client.disconnect()


@dp.message_handler(text="Все пользователи")
async def get_users(message: types.Message):
    # print(message)

    await get_all_apr_users(message, 0)


async def get_all_apr_users(msg: types.Message, mode: int):
    aus = db.select_all_ausers()
    if mode == 0:

        for au in aus:
            chat_member = await bot.get_chat_member(chat_id=au[1], user_id=au[1])
            print(chat_member.user)
            names = chat_member.user['first_name']

            keyboard = InlineKeyboardMarkup()
            # Передаем скрытый текст через параметр callback_data кнопки
            button_text = "Delete"

            message_id = msg.message_id

            print(message_id)
            hidden_text = au[0]
            callback_data = f"auser_{button_text.replace(' ', '_')}_{hidden_text}"  # Форматирование строки для уникального callback_data
            button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
            keyboard.add(button)

            await msg.answer("\n".join([
                f'Пользователь , {names}',
                f'ID : {chat_member.user.id} ',

            ]), reply_markup=keyboard)
    elif mode == 1:
        print("1")

        for au in aus:
            chat_member = await bot.get_chat_member(chat_id=au[1], user_id=au[1])
            print(chat_member.user)
            names = chat_member.user['first_name']

            await msg.answer("\n".join([
                f'Пользователь , {names}',
                f'ID : {chat_member.user.id} ',

            ]))


@dp.message_handler(text="Добавить пользователя")
async def get_add_users(message: types.Message):
    print(message)

    await FormAusers.ausers.set()

    await message.answer("Напишите ID пользователя и разрешите ему использовать это бот")


@dp.message_handler(state=FormAusers.ausers, content_types=['text'])
async def process_chats(messages: types.Message, state: FormAusers.ausers):
    # await FormChats.chats.set()
    async with state.proxy() as data:
        if messages.content_type == 'photo':
            data['text'] = messages.caption
        else:
            data['text'] = messages.text
        await state.finish()
        print(f"{data['text']}")
        wld = f"{data['text']}"
        db.add_auser(None, data['text'])
        # await FormChats.chats.set()
        await messages.answer("Пользователь добавлен в бот")


@dp.message_handler(text="Добавить чат")
async def get_users_add(message: types.Message):
    print(message)

    await FormChats.chats.set()

    await message.answer("Напишите доступный для парсинга в боте")


@dp.message_handler(text="Рабочие чаты")
async def get_users_add(message: types.Message):
    await gets_chats(message, 0)


async def gets_chats(message: types.Message, mode: int):
    if mode == 0:
        chats = db.select_all_chats()
        # print(chats)
        if len(chats) > 0:
            for chat in chats:
                # print(chat)

                keyboard = InlineKeyboardMarkup()
                button_text = "Delete"
                message_id = message.message_id
                hidden_text = chat[0]
                callback_data = f"buttons_{button_text.replace(' ', '_')}_{hidden_text}"  # Форматирование строки для уникального callback_data
                button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
                keyboard.add(button)
                await message.answer(chat[1], reply_markup=keyboard)
    elif mode == 1:
        chatso = db.select_all_chats()
        await message.answer("Измененный список чатов")
        for ww in chatso:
            # all_worlds.append(ww[1])
            await message.answer(ww[1])

        # await message.answer("Чтобы добавить разрешенный чат напишите его название и добавьте в бота")


# @dp.callback_query_handler(lambda callback_query: True)
# async def process_callbacks(callback_query: types.CallbackQuery):
#     print(callback_query)


@dp.message_handler(state=FormChats.chats, content_types=['text'])
async def process_chats(messages: types.Message, state: FormChats.chats):
    # await FormChats.chats.set()
    async with state.proxy() as data:
        if messages.content_type == 'photo':
            data['text'] = messages.caption
        else:
            data['text'] = messages.text
        await state.finish()
        print(f"{data['text']}")
        wld = f"{data['text']}"
        db.add_chats(None, wld)
        # await FormChats.chats.set()
        await messages.answer("Чат добавлен и доступен для парсинга")
