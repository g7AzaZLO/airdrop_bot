from DB.mongo import admins_collection
from settings.logging_config import get_logger

logger = get_logger()


async def get_all_admins() -> list:
    """
    Получает всех администраторов из коллекции `admins_collection`.

    Функция выполняет запрос ко всем документам в коллекции `admins_collection`,
    преобразует их в список и возвращает список идентификаторов администраторов.

    Возвращает:
    - list: Список идентификаторов администраторов.
    """
    try:
        logger.debug("Запрос всех администраторов из коллекции.")
        admins_cursor = admins_collection.find()
        admins_list = await admins_cursor.to_list(length=None)
        admin_ids = [admin["_id"] for admin in admins_list]
        logger.debug(f"Получено {len(admin_ids)} администраторов.")
        return admin_ids
    except Exception as e:
        logger.error(f"Ошибка при получении списка администраторов: {e}")
        return []
