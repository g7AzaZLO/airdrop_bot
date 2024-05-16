import asyncio
from aiogram import Dispatcher
from settings.config import bot
from handlers.standart_handler import standard_handler_router
from handlers.state_handler import state_handler_router
# from handlers.game_commands import setup_game_routes
from logic.task import task_router
from dotenv import load_dotenv
from DB.database_logic import initialize_db, get_all_tasks, insert_tasks, insert_admin_messages
from aiogram.fsm.storage.memory import MemoryStorage
from tasks.task_dict import update_tasks

# Загрузка переменных окружения
env_path = '.env'
load_dotenv(env_path)

# Инициализация хранилища состояний
storage = MemoryStorage()

# Инициализация бота
dp = Dispatcher(storage=storage)

dp.include_router(standard_handler_router)
dp.include_router(state_handler_router)
dp.include_router(task_router)
# setup_game_routes(dp)


async def change_tasks():
    while True:
        new_tasks = await get_all_tasks()
        print("Tasks have been updated.")
        await update_tasks(new_tasks)  # TODO напоминалка поставить 10 мин а не 1 перед окончательной установкой
        await asyncio.sleep(60)  # 10 минут = 600 секунд


async def main() -> None:
    await initialize_db()
    await insert_tasks()
    await insert_admin_messages(admin_messages={})
    asyncio.create_task(change_tasks())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
