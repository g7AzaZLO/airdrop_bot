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
        "ENG": """
Total supply for airdrop *{airdrop_total}* ${coin_symbol}

For participation in airdrop you get {airdrop_amount} points
For each referral you get {referral_reward} points

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
Всего выделено *{airdrop_total}* ${coin_symbol} на аирдроп

За участие в аирдропе вам начисляется {airdrop_amount} поинтов
За каждого реферала вам начисляется {referral_reward} поинтов

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
    "SMARTCONTRACT_TEXT": {
        "ENG": """
35% of the total supply is locked in the smart contract = 350,000,000 ${coin_symbol}

The smart contract rewards holders who have <b>more than 100,000 ${coin_symbol}.</b>

Rewards distribution occurs once every T period. This period can be calculated by the formula:

<code>
T = max(30 - (29 * (holder_count - 1) / 49999), 1)
</code>
<i>holder_count - the number of token holders, and T is measured in days.</i>

If a holder has more than 100,000 ${coin_symbol} in their balance, they are assigned a weight:

<code>
weight = balance / 100000
</code>
<i>where balance is the number of tokens in the holder's balance.</i>
		""",
        "RU": """
В смартконтракте заблокировано 35% всего саплая = 350 000 000 ${coin_symbol}

Смартконтракт награждает холдеров, на счету которых лежит <b>более 100 000 ${coin_symbol}.</b>

Распределение наград происходит раз в T период. Этот период можно вычислить по формуле:

<code>
T = max(30 - (29 * (holder_count - 1) / 49999), 1)
</code>
<i>holder_count - количество холдеров токена, а само T измеряется в днях.</i>

Если холдер держит более 100000 ${coin_symbol} на балансе, то ему присваивается вес:

<code>
weight = balance / 100000
</code>
<i>где balance - количество токенов на балансе холдера.</i>
		"""
    }
}
