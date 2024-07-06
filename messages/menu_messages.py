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
        "ENG": """
GOICHEV POINTS DROP 😎 SEASON 1

How to avoid becoming a goy and getting shaved by Ondrej's company, DFW Bals? The easiest way is to earn points!

Earn GOICHEV points by performing various tasks and inviting friends and acquaintances. With GOICHEV points, you will be able to receive a $GOICHEV airdrop in the future.
        """,
        "RU": """
GOICHEV POINTS DROP 😎 SEASON 1

Как не стать гоем и не быть побритым компанией Ондрея, DFW Bals? Cамый простой способ – фармить поинты!

Зарабатывайте GOICHEV-поинты, выполняя различные задания и приглашая друзей и знакомых. За GOICHEV-поинты в дальнейшем можно будет получить эирдроп $GOICHEV.
        """
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
    "FAQ_TEXT": {
    "ENG": """
1. What is $GOICHEV?
$GOICHEV is the internal meme-token of the Ondrej Goichev project, which has not yet been listed on DEX/CEX exchanges.

2. What are GOICHEV points?
GOICHEV points are points that will be converted into $GOICHEV tokens after the season is over.

3. Who is Ondrej GOICHEV? What is the company DFW Bals?
Ondrej Goichev is a fictional meme character inspired by Andrey Grachev and his company DWF Labs, but not related to them.

4. How can I avoid becoming a goy hamster?
You need to farm GOICHEV points and prepare your TONs to exchange them for $GOICHEV and become a holder!

5. Can I become as awesome as Ondrej?
Yes, if you hold a significant portion of $GOICHEV tokens.

6. If I hold $GOICHEV tokens, will I get an internship at DFW Bals?
Possibly.

7. What will be the total supply of $GOICHEV coins?
1,000,000,000,000 $GOICHEV.

8. How much will be allocated to the airdrop?
2% = 20,000,000 $GOICHEV.
    """,
    "RU": """
1. Что такое $GOICHEV?
$GOICHEV — это внутренний мем-токен проекта Ondrej Goichev, который еще не залистился на DEX/CEX биржи. После листинга можно будет обменивать $GOICHEV на $TON и наоборот.

2. Что такое GOICHEV-поинты?
GOICHEV-поинты — это очки, которые будут конвертированы в токены $GOICHEV после завершения сезона.

3. Кто такой Ондрей Гойчев? Что за компания DFW Bals?
Ондрей Гойчев — это вымышленный мем-персонаж, посвященный Андрею Грачеву и его ММ-компании DWF Labs, НО никак не связан с ними!

4. Как не стать хомяком гоем?
Нужно фармить GOICHEV-поинты и готовить свои TON’ы, чтобы обменять их на $GOICHEV и стать холдером!

5. Я смогу стать таким же крутым как Ондрей?
Да, если будешь удерживать значительное количество токенов $GOICHEV.

6. Если я держу токены $GOICHEV, меня возьмут на стажировку в DFW Bals?
Возможно.

7. Каково будет общее предложение монет $GOICHEV?
1,000,000,000,000 $GOICHEV.

8. Сколько будет выделено на airdrop?
2% = 20,000,000 $GOICHEV.
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
