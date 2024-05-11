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
TOTAL_TASKS = 9
# Links
TWITTER_LINKS = "\n".join(["https://twitter.com/buyordie_ton"])
TELEGRAM_LINKS = "\n".join(["https://t.me/buyordie_ton", "https://t.me/buyordie_chat"])
WEBSITE_URL = "https://buyordie.fun/"
MAX_USERS = 100000
MAX_REFS = 100

# Admins
ADMIN_USERNAME = "\n".join(os.getenv("ADMIN_USERNAME").split(","))

# Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("AI_KEY")

# Bot
bot = Bot(token=BOT_TOKEN)

# mongo
DB_URI = os.getenv("DB_URI")
