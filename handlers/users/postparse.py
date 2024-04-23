from aiogram.bot import bot
from telethon import TelegramClient, sync, events

from data import config
from handlers.users import scraper
# from loader import db, dp, client_tg
#
# INPUT_CHANNEL = 'Инсталогия Чат'
# OUTPUT_CHANNEL = 'output_channel_username'
# TAGS = ['#TAG1', '#TAG2']
#
# input_channels_entities = ["Инсталогия Чат","TON Community Чат"]
#
# client = client_tg
#
#
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
