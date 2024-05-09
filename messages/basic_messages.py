from settings.config import *

messages = {
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
        "referral_link": "https://t.me/Rcrvynjibot"

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
    "LANGUAGE_CHOOSE": {
        "ENG": "Please choose your language",
        "RU": "Пожалуйста, выберите ваш язык",
    },
    "PROFILE_MENU": {
        "ENG": "Your name is {user_name}",
        "RU": "Ваше имя {user_name}"
    },
    "MENU": {
        "ENG": "Here is what we have for you:",
        "RU": "Вот что у нас для Вас есть:"
    },
    "CAPTCHA_MESSAGE": {
        "ENG": "Please type in the numbers on the image",
        "RU": "Пожалуйста, введите числа на картинке"
    },

    "WELCOME_MESSAGE": {
        "ENG": """
Hello, {user_name}! I am your friendly {coin_name} Airdrop bot

Total tokens allocated to airdrop:  *50,000,000 ${coin_symbol}*

⭐️ For Joining - Get *{airdrop_amount}* point
⭐️ For each referral - Get *{referral_reward}* point

📘_By Participating you are agreeing to the {coin_name} (Airdrop) Program Terms and Conditions. Please see pinned post for more information.
Click "🚀 Join Airdrop" to proceed_
	        """,
        "RU": """
Привет, {user_name}! Я твой дружелюбный {coin_name} аирдроп бот

Общее количество токенов, выделенных для аирдропа:  *50,000,000 ${coin_symbol}*

⭐️ За присоединение - Получи *{airdrop_amount}* баллов
⭐️ За каждого реферала - Получи *{referral_reward}* баллов
	        """
    },

    "PROCEED_MESSAGE": {
        "ENG": """
📢*Airdrop Rules*

✏️ *Mandatory Tasks*:
- Join our Telegram group(s)
- Follow our Twitter page(s)

😡*Prohibited by the rules*:
- Unsubscribe from the channel
- Leave the project chat

_NOTE: Users found cheating would be disqualified & banned immediately._

{website_url}
	        """,
        "RU": """
📢*Правила аирдропа*

✏️ *Обязательные задания*:
- Вступить в наши телеграм группы
- Подписаться на наш твиттер

😡*Правилами запрещается*:
- Отписываться от твиттера/телеграмма
- Выходить из чата проекта

_ВНИМАНИЕ: Пользователи которые читерят будут удалены и забанены._

{website_url}
	        """
    },

    "MAKE_SURE_TELEGRAM": {
        "ENG": """
🔹 Subscribe to our channel and join the chat room
{telegram_links}
			""",
        "RU": """
🔹 Подпишись на наш телеграм и вступи в чат
{telegram_links}
			"""
    },

    "FOLLOW_TWITTER_TEXT": {
        "ENG": """
🔹 Follow our Twitter page
{twitter_links}
			""",
        "RU": """
🔹 Подпишись на наш Твиттер
{twitter_links}
			"""
    },

    "GET_TWITTER_LINK_TEXT": {
        "ENG": """
Type in the link to your Twitter profile to proceed.

Example: 
https://twitter.com/example
""",
        "RU": """
Введите ссылку на ваш профиль Твиттера, чтобы продолжить.
Пример:
https://twitter.com/example
"""
    },

    "SUBMIT_ADDRESS_TEXT": {
        "ENG": """
Type in your Wallet Address

Please make sure your wallet supports the *{airdrop_network}*

Example:
UQBxCOstPWvIADbaYYBapGhwfRZCEZUui5p2OEFHU0a\_wWem
			""",
        "RU": """
Введите ваш адрес кошелька

Пожалуйста убедитесь что адрес поддерживает сеть *{airdrop_network}*

Пример:
UQBxCOstPWvIADbaYYBapGhwfRZCEZUui5p2OEFHU0a\_wWem
			"""
    },

    "JOINED_TEXT": {
        "ENG": """
*Thank you!*

Rewards would be sent out automatically to your {airdrop_network} address

*Don't forget to*:
🔸 Stay in the telegram channels
🔸 Follow all the social media channels for the updates

Your personal referral link (+*{referral_reward}* point for each referral)
{referral_link}
			""",
        "RU": """
*Спасибо вам!*

Награды будут автоматически отправлены на ваш {airdrop_network} адрес, после завершения аирдропа

*Не забывайте, что необходимо*:
🔸 Оставаться в телеграм и твиттер канале
🔸 Подписаться на все соц сети, чтобы знать актуальную информацию

Ваша персональная реферальная ссылка (+*{referral_reward}* поинтов за каждого реферала)
{referral_link}
			"""
    },
    "INVALID_ADDRESS_TEXT": {
        "ENG": """
Please provide a valid crypto address.
""",
        "RU": """
Пожалуйста введите корректный адресс
		"""
    },
    "TWITTER_INVALID_LINK_TEXT": {
        "ENG": """
Please provide a valid Twitter link.
""",
        "RU": """
Пожалуйста введите корректную ссылку на Твиттер
		"""
    },
    "TWITTER_ALREADY_REGISTERED_TEXT": {
        "ENG": """
This link is already registered
""",
        "RU": """
Данный пользователь уже зарегистрирован
		"""
    },

    "NOT_SUB_AT_GROUP_TEXT": {
        "ENG": """
First, subscribe to the channel
""",
        "RU": """
Для начала подпишитесь на группы
		"""
    },

    "UKNOWN_COMMAND_TEXT": {
        "ENG": """
Unknown command, please choose from the menu.
""",
        "RU": """
Неизвестная команда, пожалуйста выберите команду из меню
		"""
    },
    "START_AGAIN_TEXT": {
        "ENG": """
Please, type /start or click the button below to begin
""",
        "RU": """
Пожалуйста, напишите /start или нажмите на кнопку ниже, чтобы начать
		"""
    },
    "ADDRESS_ALREADY_REGISTERED_TEXT": {
        "ENG": """
This address is already registered
""",
        "RU": """
Данный адрес уже зарегистрирован
		"""
    },

}
