from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    try:
        db.create_table_users()
        db.create_table_worlds()
        db.create_table_chats()
        db.create_table_allowed_users()
        # db.create_table_coffe()
        # db.create_table_qrcode()
        # db.addCode(11, "ZEDGE"

    except Exception as ex:
        print(ex)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

