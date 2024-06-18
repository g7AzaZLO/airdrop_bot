import os
from aiogram import Bot
from dotenv import load_dotenv

# ENV
env_path = '.env'
load_dotenv(env_path)

# General
COIN_SYMBOL = "GOICHEV"
COIN_NAME = "Ondrei Goichev"
AIRDROP_TOTAL = 50000000
REFERRAL_REWARD = 1000
AIRDROP_AMOUNT = 10000
AIRDROP_NETWORK = "TON"
DATABASE_FILE = "airdrop.db"
BOT_NICKNAME = "goichev_bot"

# Links
TWITTER_LINKS = "\n".join(["https://x.com/ondreigoichev"])
TELEGRAM_LINKS = "\n".join(["https://t.me/ondreigoichev_ton",]) #"https://t.me/ondreigoichev"
WEBSITE_URL = "https://goichev.xyz/"
MAX_USERS = 100000
MAX_REFS = 100

# Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("AI_KEY")

# Admins
ADMINS_IDS_INIT = [int(id.strip()) for id in os.getenv("ADMINS_IDS").split(",")]

# Bot
bot = Bot(token=BOT_TOKEN)

# mongo
DB_URI = os.getenv("DB_URI")

tasks_init = {
    1: {
        'description': {
            "ENG": """
    🔹 *Follow our Twitter page*:
    [https://x.com/ondreigoichev]
            """,
            "RU": """
    🔹 *Подпишитесь на наш Twitter*:
    [https://x.com/ondreigoichev]
            """
        },
        'image': '',
        'points': 100,
        'type': 'twitter_sub',
        'protection': 'twitter_screen_check'
    }
    # 4: {
    #     "image": "",
    #     "description": {
    #         "RU": "Оставьте комментарий в Telegram",
    #         "ENG": "Leave a comment on Telegram"
    #     },
    #     "points": 200,
    #     "type": "telegram_comment",
    #     "protection": "screen_check"
    #
}

IMAGE_PATHS = {
    "profile": "AgACAgIAAxkBAAIkBWZx-93aJkUGV7Phbb7L05_WR2OwAAJO4DEbY1eQS30lVBAqYZKHAQADAgADeQADNQQ",
    "info": "AgACAgIAAxkBAAIkBmZx--0xL9TIw_wCpplzDCBfUhWaAAJP4DEbY1eQSxkYOK-HT2GJAQADAgADeQADNQQ",
    "invite": "AgACAgIAAxkBAAIkB2Zx_AYo4mX9tpA5oocGczl7PH6PAAJR4DEbY1eQS1oUPsTZd95ZAQADAgADeQADNQQ",
    "balance": "AgACAgIAAxkBAAIkCGZx_BCEST2y5BTWFIfW8TdJOQABBAACUuAxG2NXkEt85cnpEAvb4wEAAwIAA3kAAzUE",
    "tasks": "AgACAgIAAxkBAAIkCWZx_B0NDlpWlMmWwtk7QKIuKC-aAAJT4DEbY1eQSzUNiwTrQ5g5AQADAgADeQADNQQ",
    "tokenomics": "AgACAgIAAxkBAAIkCmZx_CimB3PIsC2iO6MSFDijBj9sAAJU4DEbY1eQS1nid5PUd3wxAQADAgADeQADNQQ",
}
