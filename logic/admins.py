import os

from DB.get_all_admins import get_all_admins

ADMINS_IDS = []


async def update_admins_ids() -> None:
    global ADMINS_IDS
    ADMINS_IDS.clear()
    ADMINS_IDS.extend(await get_all_admins())
