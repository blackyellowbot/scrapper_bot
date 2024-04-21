from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

menuAdmin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Слова"),
            KeyboardButton(text="Добавить слово"),

        ],
        [
            KeyboardButton(text="Рабочие чаты"),
            KeyboardButton(text="Добавить чат"),


        ],
        [
            KeyboardButton(text="Все пользователи"),
            KeyboardButton(text="Добавить пользователя"),
        ],
        [
            KeyboardButton(text="Проверить посты"),
        ]
    ],
    resize_keyboard=True

)
menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Проверить посты"),
        ]
    ],
    resize_keyboard=True

)

users = InlineKeyboardMarkup(
  inline_keyboard=[
    [
      InlineKeyboardButton(text="Пользователь", callback_data="la"),


    ]
  ]
)