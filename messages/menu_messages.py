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
    "INFORMATION_TEXT": {
        "ENG": """
*Name*: {user_name}
*Referrals*: {refferal_number}
*TON address*: {address}
*Twitter*: {user_twitter_link}
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
{referral_link}      
        """,
        "RU": """
*Ваша реферальная ссылка*
{referral_link}
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
}
