from DB.mongo import admins_collection


async def get_all_admins() -> list:
    admins_cursor = admins_collection.find()
    admins_list = await admins_cursor.to_list(length=None)
    admin_ids = [admin["_id"] for admin in admins_list]
    return admin_ids