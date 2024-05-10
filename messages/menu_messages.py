from settings.config import *

menu_messages = {
	"default_values": {
		"user_name": "Friend",
		"coin_name": COIN_NAME,
		"coin_symbol": COIN_SYMBOL,
		"airdrop_amount": AIRDROP_AMOUNT,
		"referral_reward": REFERRAL_REWARD,
		"website_url": WEBSITE_URL,
		"telegram_links": TELEGRAM_LINKS,
		"twitter_links": TWITTER_LINKS,
		"airdrop_network": AIRDROP_NETWORK,
		"referral_link": "https://t.me/Rcrvynjibot",
		"referral_number": "0",
		"address": "address",
		"user_twitter_link": "https://twitter.com/user",
		"user_balance": "0",
		"user_referral_balance": "0",
	},
	"MENU_SETTINGS": {
		"ENG": "You can change your settings here",
		"RU": "Вы можете изменить настройки здесь",
	},
	"YES_NO": {
		"ENG": "Are you sure?",
		"RU": "Вы уверены?",
	},
	"CANCEL_JOINING": {
		"ENG": """
We are sorry to see you go. Please come back anytime.
Thank you for your support!
p.s. You are safely deleted from our database.
        """,
		"RU": """
Нам жаль, что вы уходите. Пожалуйста, заходите в любое время.
Спасибо за вашу поддержку!
p.s. Вы благополучно удалены из нашей базы данных.
        """,
	},
	"LANGUAGE_CHOSEN_WRONG": {
		"ENG": "That language is not on the list.\nPlease choose your language",
	},
	"LANGUAGE_CHOOSE": {
		"ENG": "Please choose your language",
		"RU": "Пожалуйста, выберите ваш язык",
	},
	"INFORMATION_TEXT": {
		"ENG": "SOON",
		"RU": "Скоро"
	},
	"MENU": {
		"ENG": "Here is what we have for you:",
		"RU": "Вот что у нас для Вас есть:"
	},
	"PROFILE_MENU": {
		"ENG": """
*Name*: [{user_name}]
*Referrals*: [{refferal_number}]
*TON address*: [{address}]
*Twitter*: [{user_twitter_link}]
""",
		"RU": """
*Имя*: [{user_name}]
*Рефералов*: {refferal_number}
*TON адрес*: [{address}]
*Твиттер*: [{user_twitter_link}]
        """,
	},
	"INVITE_FRIENDS_TEXT": {
		"ENG": """
*Here is your referral link*
[{referral_link}]    
        """,
		"RU": """
*Ваша реферальная ссылка*
[{referral_link}]
        """,
	},
	"BALANCE_TEXT": {
		"ENG": """
*Balance*: {balance}
*Referral poitns*: {user_referral_balance}
        """,
		"RU": """
Баланс*: {balance}
*Очки за рефералов*: {user_referral_balance}*
        """,
	},
	"UNKNOWN_COMMAND_TEXT": {
		"ENG": """
Unknown command, please choose from the menu.
""",
		"RU": """
Неизвестная команда, пожалуйста выберите команду из меню
		"""
	},
}
