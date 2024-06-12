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
        "airdrop_total": AIRDROP_TOTAL,
        "referral_link": "https://t.me/Rcrvynjibot",
        "referral_number": "0",
        "address": "address",
        "user_twitter_link": "https://twitter.com/user",
        "user_balance": "0",
        "user_referral_balance": "0",
    },
    "MENU_SETTINGS": {
        "ENG": "You can change your settings here.",
        "RU": "Вы можете изменить настройки здесь.",
    },
    "YES_NO": {
        "ENG": "Are you sure?",
        "RU": "Вы уверены?",
    },
    "CANCEL_JOINING": {
        "ENG": """
We are sorry to see you go. Please come back anytime.
Thank you for your support!
p.s. Your data has been safely removed from our database.
        """,
        "RU": """
Нам жаль, что вы уходите. Пожалуйста, заходите в любое время.
Спасибо за вашу поддержку!
p.s. Ваши данные успешно удалены из нашей базы.
        """,
    },
    "LANGUAGE_CHOSEN_WRONG": {
        "ENG": "That language is not on the list.\nPlease choose your language.",
        "RU": "Этот язык не в списке.\nПожалуйста, выберите ваш язык.",
    },
    "LANGUAGE_CHOOSE": {
        "ENG": "Please choose your language.",
        "RU": "Пожалуйста, выберите ваш язык.",
    },
    "INFORMATION_TEXT": {
        "ENG": """
Total supply for airdrop: *{airdrop_total}* ${coin_symbol}

For participation in airdrop, you receive {airdrop_amount} points.
For each referral, you get {referral_reward} points.

📢*Airdrop Rules*

✏️ *Mandatory Tasks*:
- Join our Telegram group(s)

😡*Prohibited*:
- Unsubscribing from the channel
- Leaving the project chat

_NOTE: Users found cheating will be disqualified and banned immediately._

{website_url}
		""",
        "RU": """
Всего на аирдроп выделено: *{airdrop_total}* ${coin_symbol}

За участие в аирдропе Вы получаете {airdrop_amount} очков.
За каждого реферала Вы получаете {referral_reward} очков.

📢*Правила аирдропа*

✏️ *Обязательные задания*:
- Вступить в наши группы в Telegram

😡*Запрещено*:
- Отписываться от наших каналов
- Выходить из чата проекта

_ВНИМАНИЕ: Пользователи, замеченные в мошенничестве, будут немедленно дисквалифицированы и забанены._

{website_url}
"""
    },
    "MENU": {
        "ENG": "Here is what we have for you:",
        "RU": "Вот что у нас для Вас есть:"
    },
    "PROFILE_MENU": {
        "ENG": """
*User id*: [{user_id}]
*Name*: [{user_name}]
*Referrals*: [{refferal_number}]
*TON address*: [{address}]
*Twitter*: [{user_twitter_link}]
""",
        "RU": """
*User id*: [{user_id}]
*Имя*: [{user_name}]
*Рефералы*: {refferal_number}
*TON Адрес*: [{address}]
*Twitter*: [{user_twitter_link}]
        """,
    },
    "INVITE_FRIENDS_TEXT": {
        "ENG": """
*Here is your referral link:*
[{referral_link}]    
        """,
        "RU": """
*Ваша реферальная ссылка:*
[{referral_link}]
        """,
    },
    "BALANCE_TEXT": {
        "ENG": """
*Balance*: {balance}
*Referral Poitns*: {user_referral_balance}
        """,
        "RU": """
*Баланс*: {balance}
*Очки за рефералов*: {user_referral_balance}
        """,
    },
    "UNKNOWN_COMMAND_TEXT": {
        "ENG": """
Unknown command. Please choose from the menu.
""",
        "RU": """
Неизвестная команда. Пожалуйста, выберите команду из меню.
		"""
    },
    "TOKENOMICS_TEXT": {
        "ENG": """
40% Presale
40% LP
10% Comminuty and team
5% CEX
3% For Andrei Grachev
2% Airdrop      
        """,
        "RU": """
40% Пресейл
40% Ликвидность
10% Комьюнити и команда
5% CEX
3% Для Андрея Грачева
2% Аирдроп           
        """
    },
    "CHANGE_ADDRESS_TEXT": {
        "ENG": "Are you sure you want to change your address?",
        "RU": "Вы уверены, что хотите сменить адрес?"
    },
    "GET_ADDRESS_TEXT": {
        "ENG": "Enter a new wallet address",
        "RU": "Введите новый адрес кошелька"
    },
    "SUCCESS_CHANGE_ADRESS": {
        "ENG": "The address has been successfully changed",
        "RU": "Адрес успешно изменен "
    }
}
