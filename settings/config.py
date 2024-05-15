import os
from aiogram import Bot
from dotenv import load_dotenv

# ENV
env_path = '.env'
load_dotenv(env_path)

# General
COIN_SYMBOL = "TIME"
COIN_NAME = "Buy or Die"
AIRDROP_TOTAL = 50000000
REFERRAL_REWARD = 1000
AIRDROP_AMOUNT = 10000
AIRDROP_NETWORK = "TON"
DATABASE_FILE = "airdrop.db"
BOT_NICKNAME = "Rcrvynjibot"

# Links
TWITTER_LINKS = "\n".join(["https://twitter.com/buyordie_ton"])
TELEGRAM_LINKS = "\n".join(["https://t.me/buyordie_ton", "https://t.me/buyordie_chat"])
WEBSITE_URL = "https://buyordie.fun/"
MAX_USERS = 100000
MAX_REFS = 100

# Admins
ADMINS_IDS = [int(id.strip()) for id in os.getenv("ADMINS_IDS").split(",")]
print(ADMINS_IDS)
# Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("AI_KEY")

# Bot
bot = Bot(token=BOT_TOKEN)

# mongo
DB_URI = os.getenv("DB_URI")

tasks_init = {
    1: {
        "image": "task1.png",
        "description": {
            "RU": "Подпишитесь на наш канал Telegram",
            "ENG": "Subscribe to our Telegram channel"
        },
        "points": 50,
        "type": "telegram_sub",
        "protection": None
    },
    2: {
        "image": "",
        "description": {
            "RU": "Сделайте репост нашего поста в Twitter",
            "ENG": "Retweet our post on Twitter"
        },
        "points": 100,
        "type": "twitter_retweet",
        "protection": None
    },
    3: {
        "image": "",
        "description": {
            "RU": "Оставьте комментарий в Twitter",
            "ENG": "Leave a comment on Twitter"
        },
        "points": 150,
        "type": "twitter_comment",
        "protection": "screen_check"
    },
    4: {
        "image": "",
        "description": {
            "RU": "Оставьте комментарий в Telegram",
            "ENG": "Leave a comment on Telegram"
        },
        "points": 200,
        "type": "telegram_comment",
        "protection": "screen_check"
    }
}