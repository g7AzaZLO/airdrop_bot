import asyncio
from aiogram import Dispatcher
from settings.config import bot, ADMINS_IDS_INIT
from handlers.state_handler import state_handler_router
from handlers.standart_handler import standard_handler_router, garbage_handler_router
from logic.task import task_router
from dotenv import load_dotenv
from DB.database_logic import initialize_db, insert_tasks, insert_admin_messages, add_admin
from aiogram.fsm.storage.memory import MemoryStorage
from tasks.task_dict import change_tasks


env_path = '.env'
load_dotenv(env_path)

# Инициализация хранилища состояний
storage = MemoryStorage()

# Инициализация бота
dp = Dispatcher(storage=storage)

dp.include_router(standard_handler_router)
dp.include_router(state_handler_router)
dp.include_router(garbage_handler_router)
dp.include_router(task_router)


async def main() -> None:
    await initialize_db()
    await insert_tasks()
    await insert_admin_messages(admin_messages={}, user_id=0)
    for admin in ADMINS_IDS_INIT:
        await add_admin(admin)
    await change_tasks()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
