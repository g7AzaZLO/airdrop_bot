from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu_kb = {
	'RU': ReplyKeyboardMarkup(
		keyboard=[
			[
				KeyboardButton(text="😈Профиль"),
				KeyboardButton(text="#️⃣Информация"),
			],
			[
				KeyboardButton(text="👥Пригласить друга"),
				KeyboardButton(text="💰Баланс"),
			],
			[
				KeyboardButton(text="🥇Задачи"),
				KeyboardButton(text="🔒Смартконтракт"),
			],
			[
				KeyboardButton(text="🔧Настройки"),
			],
		],
		resize_keyboard=True,
	),
	
	'ENG': ReplyKeyboardMarkup(
		keyboard=[
			[
				KeyboardButton(text="😈Profile"),
				KeyboardButton(text="#️⃣Information"),
			],
			[
				KeyboardButton(text="👥Invite Friends"),
				KeyboardButton(text="💰Balance"),
			],
			[
				KeyboardButton(text="🥇Tasks"),
				KeyboardButton(text="🔒Smartcontract"),
			],
			[
				KeyboardButton(text="🔧Settings"),
			],
		],
		resize_keyboard=True,
	)
}

kb_menu_settings = {
	'RU': ReplyKeyboardMarkup(
		keyboard=[
			[
				KeyboardButton(text="🌏Сменить Язык"),
				KeyboardButton(text="❌Удалить Аккаунт"),
			],
			[
				KeyboardButton(text="⏪Вернуться Назад"),
			],
		],
		resize_keyboard=True,
	),
	
	'ENG': ReplyKeyboardMarkup(
		keyboard=[
			[
				KeyboardButton(text="🌏Change Language"),
				KeyboardButton(text="❌Delete Account"),
			],
			[
				KeyboardButton(text="⏪Return back"),
			],
		],
		resize_keyboard=True,
	)
}


async def create_numeric_keyboard(total_buttons, exclusions, language):
    # Ensure valid inputs
    if total_buttons < 1:
        raise ValueError("Total number of buttons must be at least 1")
    
    if any(x > total_buttons or x < 1 for x in exclusions):
        raise ValueError("Exclusions contain invalid button numbers")
    
    if len(exclusions) >= total_buttons:
        raise ValueError("Number of exclusions must be less than the total number of buttons")

    # Generate list of all button numbers and then remove the exclusions
    button_numbers = set(range(1, total_buttons + 1)) - set(exclusions)

    # Determine the button prefix based on language
    prefix = "Задание #" if language == "RU" else "Task #"

    # Create buttons with language-specific labels
    keyboard_buttons = [KeyboardButton(text=f"{prefix}{num}") for num in sorted(button_numbers)]

    # Add the "Return Back" button in the appropriate language
    return_back_text = "⏪Вернуться Назад" if language == "RU" else "⏪Return Back"
    keyboard_buttons.append(KeyboardButton(text=return_back_text))

    # Organize buttons in rows of three
    keyboard = [keyboard_buttons[i:i + 3] for i in range(0, len(keyboard_buttons), 3)]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)