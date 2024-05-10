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