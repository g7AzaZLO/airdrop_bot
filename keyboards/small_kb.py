from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

join_kb = {
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Join Airdrop"), KeyboardButton(text="❌ Cancel")]
        ],
        resize_keyboard=True,
    ),
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Присоединиться к аирдропу"), KeyboardButton(text="❌ Отказаться")]
        ],
        resize_keyboard=True,
    )
}

done_cancel_kb = {
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Done"), KeyboardButton(text="❌ Cancel")]
        ],
        resize_keyboard=True,
    ),
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Принять"), KeyboardButton(text="❌ Отказаться")]
        ],
        resize_keyboard=True,
    )
}

sub_cancel_kb = {
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Submit Details"), KeyboardButton(text="❌ Cancel")]
        ],
        resize_keyboard=True,
    ),
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Согласен с правилами"), KeyboardButton(text="❌ Отказаться")]
        ],
        resize_keyboard=True,
    )
}

language_choose_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ENG English"), KeyboardButton(text="RU Русский")]
    ],
    resize_keyboard=True
)

kb_yes_no = {
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ДА"), KeyboardButton(text="НЕТ")]
        ],
        resize_keyboard=True
    ),
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="YES"), KeyboardButton(text="NO")]
        ],
        resize_keyboard=True
    )
}
