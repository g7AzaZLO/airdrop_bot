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
				KeyboardButton(text="🔀Сменить адрес"),
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
				KeyboardButton(text="🔀Change address"),
				KeyboardButton(text="⏪Return back"),
			],
		],
		resize_keyboard=True,
	)
}


async def create_numeric_keyboard(total_buttons: int, exclusions: list, language: str) -> ReplyKeyboardMarkup:
	"""
	Создает клавиатуру с числовыми кнопками и специальными кнопками управления на основе заданных параметров.

	Параметры:
	- total_buttons (int): Общее количество кнопок.
	- exclusions (list): Список номеров кнопок, которые должны быть исключены.
	- language (str): Язык для текстов кнопок ("RU" для русского, "EN" для английского).

	Возвращает:
	- ReplyKeyboardMarkup: Объект клавиатуры с созданными кнопками.
	"""
	# Ensure valid inputs
	if total_buttons < 1:
		raise ValueError("Total number of buttons must be at least 1")
	
	exclusions = [x + 1 for x in exclusions]
	
	if any(x > total_buttons or x < 1 for x in exclusions):
		raise ValueError("Exclusions contain invalid button numbers")
	
	if len(exclusions) > total_buttons:
		raise ValueError("Number of exclusions must be less than the total number of buttons")
	
	# Generate list of all button numbers and then remove the exclusions
	button_numbers = set(range(1, total_buttons + 1)) - set(exclusions)
	
	# Determine the button prefix based on language
	prefix = "Задание #" if language == "RU" else "Task #"
	
	# Create buttons with language-specific labels
	keyboard_buttons = [KeyboardButton(text=f"{prefix}{num}") for num in sorted(button_numbers)]
	
	# Prepare special buttons
	return_back_text = "⏪Вернуться Назад" if language == "RU" else "⏪Return Back"
	achievements_text = "🏆Достижения" if language == "RU" else "🏆Achievements"
	special_buttons = [KeyboardButton(text=return_back_text), KeyboardButton(text=achievements_text)]
	
	# Organize buttons in rows of three and make sure to add special buttons in the last row
	keyboard_rows = [keyboard_buttons[i:i + 3] for i in range(0, len(keyboard_buttons), 3)]
	
	keyboard_rows.append(special_buttons)
	
	return ReplyKeyboardMarkup(keyboard=keyboard_rows, resize_keyboard=True)
	# Organize buttons in rows of three until the last row
	# keyboard = [keyboard_buttons[i:i + 3] for i in range(0, len(keyboard_buttons) - (len(keyboard_buttons) % 3), 3)]
	
	# # Add the last row of buttons (if any)
	# last_buttons_row = keyboard_buttons[len(keyboard_buttons) - (len(keyboard_buttons) % 3):]
	# if len(last_buttons_row) < 3:
	# 	# If there is space in the last row, add to it
	# 	last_buttons_row.extend(special_buttons[:3 - len(last_buttons_row)])
	# 	keyboard.append(last_buttons_row)
	# 	special_buttons = special_buttons[3 - len(last_buttons_row):]
	#
	# # Ensure special buttons are on a new row if no space is available
	# if special_buttons:
	# 	keyboard.append(special_buttons)
	#
	# return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)