from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu_kb = {
	'RU': ReplyKeyboardMarkup(
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
				KeyboardButton(text="Сменить Язык"),
				KeyboardButton(text="Выйти"),
			],
		],
		resize_keyboard=True,
	),
	
	'ENG': ReplyKeyboardMarkup(
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
				KeyboardButton(text="Change Language"),
				KeyboardButton(text="Quit"),
			],
		],
		resize_keyboard=True,
	)
}
