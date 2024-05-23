import motor.motor_asyncio
from bson.objectid import ObjectId
from settings.config import DB_URI
from motor.motor_asyncio import AsyncIOMotorClient

# Настройка клиента MongoDB
DATABASE_NAME = "airdrop"
client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
db = client[DATABASE_NAME]
users_collection = db['users']
tasks_collection = db['tasks']
admin_messages_collection = db["admin_messages"]
admins_collection = db["admins"]
