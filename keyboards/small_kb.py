from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

join_kb = {
    "ENG": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀Join Airdrop", callback_data="join_airdrop"),
                InlineKeyboardButton(text="❌Cancel", callback_data="cancel")
            ]
        ]
    ),
    "RU": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀Присоединиться к аирдропу", callback_data="join_airdrop"),
                InlineKeyboardButton(text="❌Отказаться", callback_data="cancel")
            ]
        ]
    )
}

done_cancel_kb = {
    "ENG": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅Done", callback_data="done"),
                InlineKeyboardButton(text="❌Cancel", callback_data="cancel")
            ]
        ]
    ),
    "RU": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅Принять", callback_data="done"),
                InlineKeyboardButton(text="❌Отказаться", callback_data="cancel")
            ]
        ]
    )
}

sub_cancel_kb = {
    "ENG": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅Submit Details", callback_data="submit_details"),
                InlineKeyboardButton(text="❌Cancel", callback_data="cancel")
            ]
        ]
    ),
    "RU": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅Согласен с правилами", callback_data="submit_details"),
                InlineKeyboardButton(text="❌Отказаться", callback_data="cancel")
            ]
        ]
    )
}

language_choose_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ENG English", callback_data="language_eng"),
            InlineKeyboardButton(text="RU Русский", callback_data="language_ru")
        ]
    ]
)

yes_no_kb = {
    "RU": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data="yes"),
                InlineKeyboardButton(text="Нет", callback_data="no")
            ]
        ]
    ),
    "ENG": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yes", callback_data="yes"),
                InlineKeyboardButton(text="No", callback_data="no")
            ]
        ]
    )
}

social_join_kb = {
    "RU": InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅Вступил", callback_data="joined")]
        ]
    ),
    "ENG": InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅Joined", callback_data="joined")]
        ]
    )
}

kb_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Start", callback_data="start")]
    ]
)

kb_task_done_back = {
    "RU": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅Выполнил", callback_data="task_done"),
                InlineKeyboardButton(text="⏪Вернуться Назад", callback_data="return_back")
            ]
        ]
    ),
    "ENG": InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅Done", callback_data="task_done"),
                InlineKeyboardButton(text="⏪Return Back", callback_data="return_back")
            ]
        ]
    )
}

kb_tasks_back = {
    "RU": InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪Вернуться Назад", callback_data="return_back")]
        ]
    ),
    "ENG": InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪Return Back", callback_data="return_back")]
        ]
    )
}
