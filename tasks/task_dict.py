import logging
from DB.database_logic import get_all_tasks

logger = logging.getLogger(__name__)
tasks = {}


async def update_tasks(new_tasks) -> None:
    try:
        global tasks
        tasks.clear()  # Удаляем все существующие задачи
        tasks.update(new_tasks)  # Обновляем новыми задачами
        logger.debug("Tasks have been updated: %s", tasks)
    except Exception as e:
        logger.error("An error occurred while updating tasks: %s", e)


async def change_tasks() -> None:
    try:
        new_tasks = await get_all_tasks()
        logger.info("Tasks have been updated.")
        await update_tasks(new_tasks)
    except Exception as e:
        logger.error("An error occurred while changing tasks: %s", e)


protection_for_admins = ["screen_check", "twitter_screen_check"]
