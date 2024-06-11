import os

from DB.get_all_admins import get_all_admins

ADMINS_IDS = []


async def update_admins_ids() -> None:
    """
    Обновляет глобальный список идентификаторов администраторов.

    Действия:
    - Очищает текущий список идентификаторов администраторов.
    - Заполняет его новыми значениями, полученными из базы данных.
    """
    global ADMINS_IDS
    ADMINS_IDS.clear()
    ADMINS_IDS.extend(await get_all_admins())
