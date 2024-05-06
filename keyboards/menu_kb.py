from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu_kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Профиль"),
            KeyboardButton(text="Информация"),
        ],
        [
            KeyboardButton(text="Пригласить друга"),
            KeyboardButton(text="Баланс"),
        ],
        [
            KeyboardButton(text="Задачи"),
            KeyboardButton(text="Смартконтракт"),
        ],
        [
            KeyboardButton(text="Выйти"),
        ],
    ],
    resize_keyboard=True,
)

menu_kb_en = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Profile"),
            KeyboardButton(text="Information"),
        ],
        [
            KeyboardButton(text="Invite Friends"),
            KeyboardButton(text="Balance"),
        ],
        [
            KeyboardButton(text="Tasks"),
            KeyboardButton(text="Smartcontract"),
        ],
        [
            KeyboardButton(text="Quit"),
        ],
    ],
    resize_keyboard=True,
)