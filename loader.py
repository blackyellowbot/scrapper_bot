from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon import TelegramClient

from utils.db_api.sqlite import Database
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
client_tg = TelegramClient('mibotdd', config.API_ID, config.API_HASH)
