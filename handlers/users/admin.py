import time
import re

from aiogram import types

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import BotBlocked

from telethon import TelegramClient, events
from telethon.tl.types import PeerUser

from botogram import Bot as btt

from data import config
from handlers.users import scraper

from loader import dp, bot, db, client_tg

sent_messages = []

client = client_tg


class FormPost(StatesGroup):
    post = State()


class FormChats(StatesGroup):
    chats = State()


class FormChatsUrl(StatesGroup):
    chatsUrl = State()


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
    await client.start()

    wlds = db.select_all_worlds()
    wlds_all = []
    for wld in wlds:
        wlds_all.append(wld[1])
    chats = db.select_all_chats()
    all_chats = []
    for chat in chats:
        all_chats.append(chat[2])
    # print(all_chats)

    for chat in all_chats:
        # print(chat)
        time.sleep(1)
        messages = client.iter_messages(chat, limit=50)

        async for mess in messages:
            # print(message.text)
            time.sleep(1)
            found = any(word in mess.text for word in wlds_all)
            if found:
                # print(mess.text)
                try:
                    print("P")
                    user = await client.get_entity(mess.sender_id)
                except ValueError:
                    print("dd")
                    keyboard = types.InlineKeyboardMarkup()
                    button = types.InlineKeyboardButton(text="Пользователь скрыл свой ник",
                                                        callback_data="empty_button")
                    keyboard.add(button)
                    await message.answer(mess.text, reply_markup=keyboard)


                else:
                    print("Nothing went wrong")
                    await message.answer(mess.text,
                                         reply_markup=types.InlineKeyboardMarkup(
                                             inline_keyboard=[
                                                 [
                                                     types.InlineKeyboardButton(
                                                         text=f"Написать сообщение {user.username}",
                                                         url=f"https://t.me/{user.username}")
                                                 ]
                                             ]
                                         ))

    # await client.disconnect()


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
        data['name'] = messages.text
        # await state.finish()
        print(f"{data['name']}")
        # wld = f"{data['text']}"
        # db.add_chats(None, wld)
        await FormChatsUrl.chatsUrl.set()
        await messages.answer("Напишите ссылку чата")


@dp.message_handler(state=FormChatsUrl.chatsUrl, content_types=['text'])
async def process_chats(messages: types.Message, state: FormChats.chats):
    # await FormChats.chats.set()
    print(state.proxy())
    async with state.proxy() as data:
        data['url'] = messages.text
        await state.finish()
        print(f"{data}")
        urls = f"{data['url']}"
        names = f"{data['name']}"
        db.add_chats(None, names, urls)
        # await FormChatsUrl.chatsUrl.set()
        await messages.answer("Link added")


# @client.on(events.NewMessage(chats=('https://t.me/instalogiya_chat',)))
# # @client.on(events.NewMessage())
# async def normal_handler(event):
#     print(event.message)
#
#     await dp.bot.send_message(event.message)
#     # for tag in TAGS:
#     #
#     #     if tag in str(event.message):
#     #         print()
#     #
#     #      # await client.send_message(OUTPUT_CHANNEL, event.message)
#
#
# client.start()
# client.run_until_disconnected()
