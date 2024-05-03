import asyncio

from aiogram import Bot, Dispatcher
from settings.config import BOT_TOKEN

# Инициализация бота

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)  # Пропускает сообщения накопившиеся пока бот отключен
    await dp.start_polling(bot)


asyncio.run(main())
