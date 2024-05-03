import asyncio

from aiogram import Bot, Dispatcher
from settings.config import BOT_TOKEN

# Bot initial

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)  # Skip message when bot offline
    await dp.start_polling(bot)


asyncio.run(main())
