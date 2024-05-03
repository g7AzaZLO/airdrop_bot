from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

join_kb = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text="🚀 Join Airdrop"),
    ],
    resize_keyboard=True,
)

done_cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text="✅ Done"),
        KeyboardButton(text="❌ Cancel"),
    ],
    resize_keyboard=True,
)

sub_cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text="✅ Submit Details"),
        KeyboardButton(text="❌ Cancel"),
    ],
    resize_keyboard=True,
)
