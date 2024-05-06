from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

join_kb_eng = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text="🚀 Join Airdrop"),
    ],
    resize_keyboard=True,
)

join_kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text="🚀 Присоединиться к аирдропу"),
    ],
    resize_keyboard=True,
)

done_cancel_kb_eng = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text="✅ Done"),
        KeyboardButton(text="❌ Cancel"),
    ],
    resize_keyboard=True,
)

done_cancel_kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text="✅ Принять"),
        KeyboardButton(text="❌ Отказаться"),
    ],
    resize_keyboard=True,
)

sub_cancel_kb_eng = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text="✅ Submit Details"),
        KeyboardButton(text="❌ Cancel"),
    ],
    resize_keyboard=True,
)

sub_cancel_kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text="✅ Согласен с правилами"),
        KeyboardButton(text="❌ Отказаться"),
    ],
    resize_keyboard=True,
)

language_choose_kb = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text="ENG English"),
        KeyboardButton(text="RU Русский"),
    ]
)