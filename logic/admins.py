import os
from settings.logging_config import get_logger
from DB.get_all_admins import get_all_admins

logger = get_logger()

ADMINS_IDS = []


async def update_admins_ids() -> None:
    """
    Обновляет глобальный список идентификаторов администраторов.

    Действия:
    - Очищает текущий список идентификаторов администраторов.
    - Заполняет его новыми значениями, полученными из базы данных.
    """
    global ADMINS_IDS
    try:
        logger.info("Starting update of admin IDs.")
        ADMINS_IDS.clear()
        admins = await get_all_admins()
        ADMINS_IDS.extend(admins)
        logger.info(f"Updated admin IDs: {ADMINS_IDS}")
    except Exception as e:
        logger.error(f"Error updating admin IDs: {e}")
