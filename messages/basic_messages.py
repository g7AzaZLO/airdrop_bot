from settings.config import *

messages = {
    "default_values": {
        "user_name": "Friend",
        "coin_name": COIN_NAME,
        "coin_symbol": COIN_SYMBOL,
        "airdrop_amount": AIRDROP_AMOUNT,
        "referral_reward": REFERRAL_REWARD,
        "airdrop_total": AIRDROP_TOTAL,
        "website_url": WEBSITE_URL,
        "telegram_links": TELEGRAM_LINKS,
        "twitter_links": TWITTER_LINKS,
        "airdrop_network": AIRDROP_NETWORK,
        "referral_link": "https://t.me/goichev_bot"
    },

    "CAPTCHA_MESSAGE": {
        "ENG": "Please type in the numbers on the image.",
        "RU": "Пожалуйста, введите числа на картинке."
    },

    "WELCOME_MESSAGE": {
        "ENG": """
Hello, [{user_name}]! I am your friendly {coin_name} Airdrop bot.

Total tokens allocated to airdrop: *{airdrop_total} ${coin_symbol}*

⭐️ For joining you get *{airdrop_amount}* points
⭐️ For each referral you get *{referral_reward}* points

📘 _By participating, you agree to the {coin_name} Airdrop Program Terms and Conditions. Please see the pinned post for more information.

Click "🚀 Join Airdrop" to proceed._
        """,
        "RU": """
Привет, [{user_name}]! Я твой дружелюбный {coin_name} аирдроп бот.

Общее количество токенов, выделенных для аирдропа: *{airdrop_total} ${coin_symbol}*

⭐️ За присоединение - Получи *{airdrop_amount}* очков
⭐️ За каждого реферала - Получи *{referral_reward}* очков

📘 _Принимая участие, вы соглашаетесь с Условиями программы аирдропа {coin_name}. Пожалуйста, ознакомьтесь с закрепленным постом для получения дополнительной информации.

Нажмите "🚀 Присоединиться к аирдропу" чтобы продолжить._
        """
    },

    "PROCEED_MESSAGE": {
        "ENG": """
📢 *Airdrop Rules*

✏️ *Mandatory Tasks*:
- Join our Telegram group(s)

😡 *Prohibited*:
- Unsubscribing from the channel
- Leaving the project chat

_NOTE: Users found cheating will be disqualified and banned immediately._

{website_url}
        """,
        "RU": """
📢 *Правила аирдропа*

✏️ *Обязательные задания*:
- Вступить в наши группы в Telegram

😡 *Запрещено*:
- Отписываться от наших каналов
- Выходить из чата проекта

_ВНИМАНИЕ: Пользователи, замеченные в мошенничестве, будут немедленно дисквалифицированы и забанены._

{website_url}
        """
    },

    "MAKE_SURE_TELEGRAM": {
        "ENG": """
    Join the official Telegram channel [@ondreigoichev_ton]. Once done, click the "Joined" button.
        """,
        "RU": """
    Присоединитесь к официальному телеграм-каналу [@ondreigoichev_ton]. После этого нажмите кнопку «Вступил».
        """
    },

    "FOLLOW_TWITTER_TEXT": {
        "ENG": """
*Follow our Twitter page*:
[{twitter_links}]

Type in the link to your Twitter profile to proceed.

*Example*:
https://twitter.com/example
https://x.com/example

_WARNING: this tweet will be used to verify assignments_
        """,
        "RU": """
*Подпишитесь на наш Twitter*:
[{twitter_links}]

Введите ссылку на ваш профиль в Twitter, чтобы продолжить.

*Пример*:
https://twitter.com/example
https://x.com/example

_ВНИМАНИЕ: данный твиттер будет использоваться для проверки заданий_
        """
    },

    "SUBMIT_ADDRESS_TEXT": {
        "ENG": """
Type in your wallet address.

Please make sure your wallet supports the *{airdrop_network}*.

Example:
[UQBxCOstPWvIADbaYYBapGhwfRZCEZUui5p2OEFHU0a_wWem]
IMPORTANT: Use non-custodial wallets [(e.g. Tonkeeper, MyTonWallet). Do not use exchange wallets (TON Space is okay).]
        """,
        "RU": """
Введите ваш адрес кошелька.

Пожалуйста, убедитесь, что ваш кошелек поддерживает сеть *{airdrop_network}*.

Пример:
[UQBxCOstPWvIADbaYYBapGhwfRZCEZUui5p2OEFHU0a_wWem]

ВАЖНО: Используйте некастодиальные кошельки [(например, Tonkeeper, MyTonWallet). Не используйте кошельки бирж (TON Space можно).]
        """
    },

    "LINK_WALLET": {
        "ENG": """
You have successfully linked your wallet!
[{address}]
        """,
        "RU": """
Вы успешно привязали кошелек!
[{address}]
        """
    },

    "INVALID_ADDRESS_TEXT": {
        "ENG": "Please provide a valid crypto address.",
        "RU": "Пожалуйста, введите корректный адрес кошелька."
    },

    "TWITTER_INVALID_LINK_TEXT": {
        "ENG": "Please provide a valid Twitter link.",
        "RU": "Пожалуйста, введите корректную ссылку на Twitter."
    },

    "TWITTER_ALREADY_REGISTERED_TEXT": {
        "ENG": "This Twitter link is already registered.",
        "RU": "Данный профиль Twitter уже зарегистрирован."
    },

    "ADDRESS_ALREADY_REGISTERED_TEXT": {
        "ENG": "This address is already registered.",
        "RU": "Данный адрес уже зарегистрирован."
    },

    "NOT_SUB_AT_GROUP_TEXT": {
        "ENG": "First, subscribe to the channel: {telegram_links}",
        "RU": "Сначала подпишитесь на канал: {telegram_links}"
    },

    "START_AGAIN_TEXT": {
        "ENG": "Please, type /start  to begin.",
        "RU": "Пожалуйста, введите /start чтобы начать."
    },
    "MENU_GOICHEV": {
        "ENG": """
GOICHEV POINTS DROP 😎 SEASON 1

How to avoid becoming a <s>hamster</s> goy and getting shaved by Ondrej's company, DFW Bals? The easiest way is to earn points!

Earn GOICHEV points by performing various tasks and inviting friends and acquaintances. With GOICHEV points, you will be able to receive a $GOICHEV airdrop in the future.
        """,
        "RU": """
GOICHEV POINTS DROP 😎 SEASON 1

Как не стать <s>хомяком</s> гоем и не быть побритым компанией Ондрея, DFW Bals? Cамый простой способ – фармить поинты!

Зарабатывайте GOICHEV-поинты, выполняя различные задания и приглашая друзей и знакомых. За GOICHEV-поинты в дальнейшем можно будет получить эирдроп $GOICHEV.
        """
    }
}
