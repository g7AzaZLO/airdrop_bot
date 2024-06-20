from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu_kb = {
    'RU': InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="😈Профиль", callback_data="profile"),
                InlineKeyboardButton(text="#️⃣Информация", callback_data="information"),
            ],
            [
                InlineKeyboardButton(text="👥Пригласить друга", callback_data="invite_friends"),
                InlineKeyboardButton(text="💰Баланс", callback_data="balance"),
            ],
            [
                InlineKeyboardButton(text="🥇Задачи", callback_data="tasks"),
                InlineKeyboardButton(text="🔒FAQ", callback_data="faq"),
            ],
            [
                InlineKeyboardButton(text="🔧Настройки", callback_data="settings"),
            ],
        ]
    ),

    'ENG': InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="😈Profile", callback_data="profile"),
                InlineKeyboardButton(text="#️⃣Information", callback_data="information"),
            ],
            [
                InlineKeyboardButton(text="👥Invite Friends", callback_data="invite_friends"),
                InlineKeyboardButton(text="💰Balance", callback_data="balance"),
            ],
            [
                InlineKeyboardButton(text="🥇Tasks", callback_data="tasks"),
                InlineKeyboardButton(text="🔒FAQ", callback_data="faq"),
            ],
            [
                InlineKeyboardButton(text="🔧Settings", callback_data="settings"),
            ],
        ]
    )
}

kb_menu_settings = {
    'RU': InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌏Сменить Язык", callback_data="change_language"),
                InlineKeyboardButton(text="❌Удалить Аккаунт", callback_data="delete_account"),
            ],
            [
                InlineKeyboardButton(text="🔀Сменить адрес", callback_data="change_address"),
                InlineKeyboardButton(text="⏪Вернуться Назад", callback_data="return_back"),
            ],
        ]
    ),

    'ENG': InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌏Change Language", callback_data="change_language"),
                InlineKeyboardButton(text="❌Delete Account", callback_data="delete_account"),
            ],
            [
                InlineKeyboardButton(text="🔀Change address", callback_data="change_address"),
                InlineKeyboardButton(text="⏪Return back", callback_data="return_back"),
            ],
        ]
    )
}


async def create_numeric_keyboard(total_buttons: int, exclusions: list, language: str) -> InlineKeyboardMarkup:
    if total_buttons < 1:
        raise ValueError("Total number of buttons must be at least 1")

    exclusions = [x + 1 for x in exclusions]

    if any(x > total_buttons or x < 1 for x in exclusions):
        raise ValueError("Exclusions contain invalid button numbers")

    if len(exclusions) > total_buttons:
        raise ValueError("Number of exclusions must be less than the total number of buttons")

    button_numbers = set(range(1, total_buttons + 1)) - set(exclusions)
    prefix = "Задание #" if language == "RU" else "Task #"
    keyboard_buttons = [
        InlineKeyboardButton(text=f"{prefix}{num}", callback_data=f"task_{num}") for num in sorted(button_numbers)
    ]

    achievements_text = "🏆Достижения" if language == "RU" else "🏆Achievements"
    return_back_text = "⏪Вернуться Назад" if language == "RU" else "⏪Return Back"
    all_tasks_text = "📋Все Задания" if language == "RU" else "📋All Tasks"

    special_buttons = [
        InlineKeyboardButton(text=achievements_text, callback_data="achievements"),
        InlineKeyboardButton(text=return_back_text, callback_data="return_back_in_menu")
    ]

    keyboard_buttons.append(InlineKeyboardButton(text=all_tasks_text, callback_data="all_tasks"))
    keyboard_rows = [keyboard_buttons[i:i + 3] for i in range(0, len(keyboard_buttons), 3)]
    keyboard_rows.append(special_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
