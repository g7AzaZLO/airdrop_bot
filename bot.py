import asyncio

from aiogram import Dispatcher
from settings.config import bot
from handlers.standart_handler import standard_handler_router
from handlers.state_handler import state_handler_router
from handlers.game_commands import setup_game_routes
from logic.task import task_router
from dotenv import load_dotenv
from DB.database_logic import initialize_db


# loading the environment
env_path = '.env'  # '..\\.env.empty'
load_dotenv(env_path)

# Инициализация бота
dp = Dispatcher()

dp.include_router(standard_handler_router)
dp.include_router(state_handler_router)
dp.include_router(task_router)
setup_game_routes(dp)


async def main() -> None:
    await initialize_db() # Инициализация базы данных
    await bot.delete_webhook(drop_pending_updates=True)  # Пропускает сообщения накопившиеся пока бот отключен
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())
