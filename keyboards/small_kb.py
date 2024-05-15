from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

join_kb = {
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀Join Airdrop"), KeyboardButton(text="❌Cancel")]
        ],
        resize_keyboard=True,
    ),
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀Присоединиться к аирдропу"), KeyboardButton(text="❌Отказаться")]
        ],
        resize_keyboard=True,
    )
}

done_cancel_kb = {
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅Done"), KeyboardButton(text="❌Cancel")]
        ],
        resize_keyboard=True,
    ),
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅Принять"), KeyboardButton(text="❌Отказаться")]
        ],
        resize_keyboard=True,
    )
}

sub_cancel_kb = {
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅Submit Details"), KeyboardButton(text="❌Cancel")]
        ],
        resize_keyboard=True,
    ),
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅Согласен с правилами"), KeyboardButton(text="❌Отказаться")]
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

yes_no_kb = {
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
        ],
        resize_keyboard=True
    ),
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
        ],
        resize_keyboard=True
    )
}

social_join_kb = {
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅Вступил")]
        ],
        resize_keyboard=True
    ),
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅Joined")]
        ],
        resize_keyboard=True
    )
}

kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start")]
    ],
    resize_keyboard=True
)

kb_task_done_back = {
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅Выполнил"), KeyboardButton(text="⏪Вернуться Назад")]
        ],
        resize_keyboard=True
    ),
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅Done"), KeyboardButton(text="⏪Return Back")]
        ],
        resize_keyboard=True
    )
}

kb_tasks_back = {
    "RU": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏪Вернуться Назад")]
        ],
        resize_keyboard=True
    ),
    "ENG": ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏪Return Back")]
        ],
        resize_keyboard=True
    )
}