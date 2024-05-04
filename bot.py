import asyncio

from aiogram import Bot, Dispatcher
from settings.config import BOT_TOKEN
from handlers.standart_handler import standart_handler_router

# import os
# Инициализация бота

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(standart_handler_router)

async def main() -> None:
	await bot.delete_webhook(drop_pending_updates=True)  # Пропускает сообщения накопившиеся пока бот отключен
	await dp.start_polling(bot)


asyncio.run(main())

