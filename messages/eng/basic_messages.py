from settings.config import *

CAPTCHA_MESSAGE = {
    "ENG": "Please type in the numbers on the image",
    "RU": "Пожалуйста, введите числа на картинке"
}

WELCOME_MESSAGE = {
    "ENG": f"""
Hello, NAME! I am your friendly {COIN_NAME} Airdrop bot

Total tokens allocated to airdrop:  *50,000,000 ${COIN_SYMBOL}*

⭐️ For Joining - Get *{AIRDROP_AMOUNT}* point
⭐️ For each referral - Get *{REFERRAL_REWARD}* point

📘_By Participating you are agreeing to the {COIN_NAME} (Airdrop) Program Terms and Conditions. Please see pinned post for more information.
Click "🚀 Join Airdrop" to proceed_
""",
    "RU": f"""
Привет, NAME! Я твой дружелюбный {COIN_NAME} аирдрп бот

Общее количество токенов, выделенных для аирдропа:  *50,000,000 ${COIN_SYMBOL}*

⭐️ За присоединение - Получи *{AIRDROP_AMOUNT}* баллов
⭐️ За каждого реферала - Получи *{REFERRAL_REWARD}* баллов"""}

PROCEED_MESSAGE = {
    "ENG": f"""
📢*Airdrop Rules*

✏️ *Mandatory Tasks*:
- Join our Telegram group(s)
- Follow our Twitter page(s)

😡*Prohibited by the rules*: 
- Unsubscribe from the channel
- Leave the project chat

_NOTE: Users found cheating would be disqualified & banned immediately._

{WEBSITE_URL}
""",
    "RU": f"""
📢*Правила аирдропа*

✏️ *Обязательные задания*:
- Вступить в наши телеграм группы
- Подписаться на наш твиттер

😡*Правилами запрещается*: 
- Отписываться от твиттера/телеграмма
- Выходить из чата проекта

_ВНИМАНИЕ: Пользователи которые читерят будут удалены и забанены._

{WEBSITE_URL}
"""}

MAKE_SURE_TELEGRAM = {"ENG": f"""
🔹 Subscribe to our channel and join the chat room
{TELEGRAM_LINKS}
""",
                      "RU": f"""
🔹 Подпишись на наш телеграм и вступи в чат
{TELEGRAM_LINKS}
"""}

FOLLOW_TWITTER_TEXT = {"ENG": f"""
🔹 Follow our Twitter page
{TWITTER_LINKS}
""",
                       "RU": f"""
🔹 Подпишись на наш Твиттер
{TWITTER_LINKS}
"""}

SUBMIT_BEP20_TEXT = {"ENG": f"""
Type in your Wallet Address

Please make sure your wallet supports the *{AIRDROP_NETWORK}*

Example:
UQBxCOstPWvIADbaYYBapGhwfRZCEZUui5p2OEFHU0a\_wWem

_Incorrect Details? Use /restart command to start over_
""",
                     "RU": f"""
Введите ваш адрес кошелька

Пожалуйста убедитесь что адрес поддерживает сеть *{AIRDROP_NETWORK}*

Пример:
UQBxCOstPWvIADbaYYBapGhwfRZCEZUui5p2OEFHU0a\_wWem

_Ввели неверно? Используйте /restart команду, чтобы начать заново_
"""}

JOINED = {"ENG":f"""
*Thank you!*

Rewards would be sent out automatically to your {AIRDROP_NETWORK} address

*Don't forget to*:
🔸 Stay in the telegram channels
🔸 Follow all the social media channels for the updates

Your personal referral link (+*{REFERRAL_REWARD}* point for each referral)
REPLACEME
""",
          "RU":f"""
*Спасибо вам!*

Награды будут автоматически отправлены на ваш {AIRDROP_NETWORK} адрес, после завершения аирдропа

*Не забывайте, что необходимо*:
🔸 Оставаться в телеграм и твиттер канале
🔸 Подписаться на все соц сети, чтобы знать актуальную информацию

Ваша персональная реферальная ссылка (+*{REFERRAL_REWARD}* поинтов за каждого реферала)
REPLACEME
"""}
