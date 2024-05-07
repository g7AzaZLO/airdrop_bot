import asyncio

from aiogram import Bot, Dispatcher
from settings.config import BOT_TOKEN
from handlers.standart_handler import standard_handler_router
from handlers.state_handler import state_handler_router
from handlers.game_commands import setup_game_routes
from dotenv import load_dotenv
from DB.database_logic import initialize_db


# loading the environment
env_path = '.env'  # '..\\.env'
load_dotenv(env_path)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(standard_handler_router)
dp.include_router(state_handler_router)
setup_game_routes(dp)


async def main() -> None:
    initialize_db() # Инициализация базы данных
    await bot.delete_webhook(drop_pending_updates=True)  # Пропускает сообщения накопившиеся пока бот отключен
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())
