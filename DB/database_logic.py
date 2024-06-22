from pymongo import DESCENDING

from logic.admins import update_admins_ids
from settings.config import REFERRAL_REWARD, tasks_init
from DB.mongo import users_collection, tasks_collection, admin_messages_collection, admins_collection
from FSM.states import get_state_from_string
from settings.logging_config import get_logger

logger = get_logger()


async def initialize_db() -> None:
    """
    Инициализирует коллекцию пользователей в MongoDB.
    Создает индексы для уникальности и быстрого доступа к полям, таким как USER_ID.
    Если база данных уже существует, выводит соответствующее сообщение.
    """
    try:
        existing_indexes = await users_collection.index_information()
        if 'USER_ID_1' in existing_indexes:
            logger.info("Database already initialized with required indexes.")
        else:
            await users_collection.create_index("USER_ID", unique=True)
            logger.info("Database initialized successfully with indexes on USER_ID")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")


async def insert_tasks() -> None:
    """
    Вставляет задачи в коллекцию `tasks_collection` в базе данных MongoDB.

    Функция перебирает все задачи из словаря `tasks_init`, добавляет каждому
    из них идентификатор `_id` и вставляет их в коллекцию `tasks_collection`
    """
    try:
        for task_id, task_data in tasks_init.items():
            task_data["_id"] = task_id
            await tasks_collection.update_one({"_id": task_id}, {"$set": task_data}, upsert=True)
            logger.info(f"Task {task_id} inserted/updated successfully.")
    except Exception as e:
        logger.error(f"Error inserting tasks: {e}")


async def get_admin_messages_dict(user_id: int) -> dict:
    """
    Получает словарь сообщений администраторов из коллекции `admin_messages_collection` в базе данных MongoDB.

    Функция ищет документ в коллекции `admin_messages_collection` по `user_id`.
    Если документ не найден, возвращается пустой словарь.
    Если документ найден, извлекается список задач из поля `tasks`, и создается словарь `admin_messages_dict`,

    Параметры:
    - user_id (int): Идентификатор пользователя.

    Возвращает:
    - dict: Словарь сообщений администраторов, где ключ - идентификатор задачи, а значение - данные задачи.
    """
    try:
        user_doc = await admin_messages_collection.find_one({"user_id": user_id})
        if not user_doc:
            logger.info(f"No admin messages found for user_id: {user_id}")
            return {}
        admin_messages_dict = {task["_id"]: task for task in user_doc.get("tasks", [])}
        logger.info(f"Admin messages retrieved for user_id: {user_id}")
        return admin_messages_dict
    except Exception as e:
        logger.error(f"Error retrieving admin messages for user_id {user_id}: {e}")
        return {}


async def delete_admin_message(task_id: int, user_id: int) -> None:
    """
    Удаляет задачу из списка задач администратора в коллекции `admin_messages_collection` по идентификатору задачи и пользователя.

    Функция ищет документ в коллекции `admin_messages_collection` по `user_id`.
    Если документ не найден, функция возвращает `None`.
    Если документ найден, функция обновляет список задач, исключая задачу с заданным `task_id`.
    Если обновленный список задач не пуст, функция обновляет документ с новым списком задач.
    Если обновленный список задач пуст, функция удаляет документ из коллекции.

    Параметры:
    - task_id (int): Идентификатор задачи, которую нужно удалить.
    - user_id (int): Идентификатор пользователя.

    Возвращает:
    - None
    """
    try:
        user_doc = await admin_messages_collection.find_one({"user_id": user_id})
        if not user_doc:
            logger.info(f"No admin messages found for user_id: {user_id}")
            return
        updated_tasks = [task for task in user_doc.get("tasks", []) if task["_id"] != task_id]
        if updated_tasks:
            await admin_messages_collection.update_one(
                {"user_id": user_id},
                {"$set": {"tasks": updated_tasks}}
            )
            logger.info(f"Task with task_id: {task_id} deleted for user_id: {user_id}. Updated tasks list.")
        else:
            await admin_messages_collection.delete_one({"user_id": user_id})
            logger.info(f"All tasks deleted for user_id: {user_id}. Document removed from collection.")
    except Exception as e:
        logger.error(f"Error deleting task with task_id {task_id} for user_id {user_id}: {e}")


async def insert_admin_messages(admin_messages: dict, user_id: int) -> None:
    """
    Вставляет или обновляет сообщения администраторов в коллекции `admin_messages_collection` для конкретного пользователя.

    Функция ищет документ в коллекции `admin_messages_collection` по `user_id`.
    Если документ не найден, создается новый документ с `user_id` и пустым списком задач.
    Функция обновляет или добавляет задачи из словаря `admin_messages` в список задач документа.
    Если задача с заданным `task_id` уже существует, она обновляется.
    Если задача с заданным `task_id` не существует, она добавляется в список задач.

    Параметры:
    - admin_messages (dict): Словарь, где ключи - идентификаторы задач, а значения - данные сообщений.
    - user_id (int): Идентификатор пользователя.

    Возвращает:
    - None
       """
    try:
        user_doc = await admin_messages_collection.find_one({"user_id": user_id})
        if user_doc is None:
            user_doc = {"user_id": user_id, "tasks": []}
            logger.info(f"New user document created for user_id: {user_id}")

        tasks_dict = {task_id: message_data for task_id, message_data in admin_messages.items()}
        for task_id, message_data in tasks_dict.items():
            message_data["_id"] = task_id
            message_data["user_id"] = user_id
            message_data = {str(k): v for k, v in message_data.items()}
            task_exists = False
            for task in user_doc["tasks"]:
                if task["_id"] == task_id:
                    task.update(message_data)
                    task_exists = True
                    logger.info(f"Task with task_id: {task_id} updated for user_id: {user_id}")
                    break
            if not task_exists:
                user_doc["tasks"].append(message_data)
                logger.info(f"Task with task_id: {task_id} added for user_id: {user_id}")

        await admin_messages_collection.update_one(
            {"user_id": user_id},
            {"$set": {"tasks": user_doc["tasks"]}},
            upsert=True
        )
        logger.info(f"Admin messages updated for user_id: {user_id}")
    except Exception as e:
        logger.error(f"Error inserting admin messages for user_id {user_id}: {e}")


async def get_all_tasks() -> dict:
    """
    Получает все задачи из коллекции `tasks_collection` и возвращает их в виде словаря.

    Функция выполняет запрос ко всем документам в коллекции `tasks_collection`, преобразует их в список,
    а затем в словарь, где ключами являются идентификаторы задач (`_id`), а значениями - данные задач.

    Возвращает:
    - dict: Словарь, содержащий все задачи, где ключами являются идентификаторы задач, а значениями - данные задач.
      """
    try:
        tasks_cursor = tasks_collection.find()
        tasks_list = await tasks_cursor.to_list(length=None)
        tasks_dict = {task["_id"]: task for task in tasks_list}
        logger.info(f"Retrieved {len(tasks_dict)} tasks from the collection.")
        return tasks_dict
    except Exception as e:
        logger.error(f"Error retrieving tasks: {e}")
        return {}


async def delete_user_from_db(user_id: int) -> bool:
    """
    Удаляет пользователя из коллекции MongoDB по заданному идентификатору пользователя.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - True, если удаление прошло успешно.
    - False, если в процессе удаления произошла ошибка.
    """
    try:
        result = await users_collection.delete_one({"USER_ID": user_id})
        if result.deleted_count > 0:
            logger.info(f"User {user_id} deleted successfully.")
            return True
        else:
            logger.warning(f"User {user_id} not found in database.")
            return False
    except Exception as e:
        logger.error(f"Error deleting user {user_id} from database: {e}")
        return False


# Функция проверки наличия пользователя в базе данных
async def check_is_user_already_here(user_id: int) -> bool:
    """
    Проверяет, существует ли пользователь с заданным идентификатором в MongoDB.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - True, если пользователь существует в базе данных.
    - False, если пользователь не найден в базе данных.
    """
    try:
        user = await users_collection.find_one({"USER_ID": user_id})
        return user is not None
    except Exception as e:
        logger.error(f"Error checking if user {user_id} is already in database: {e}")
        return False


async def update_user_details(user_id: int, **kwargs) -> bool:
    """
    Обновляет конкретные детали пользователя в MongoDB. Принимает ID пользователя и аргументы,
    представляющие поля для обновления.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.
    - **kwargs: Переменные аргументы, представляющие пары "поле-значение" для обновления.

    Возвращает:
    - True, если обновление прошло успешно.
    - False, если обновление не удалось.
    """
    logger.debug("def update_user_details")
    try:
        update_fields = {key: value for key, value in kwargs.items()}
        await users_collection.update_one(
            {"USER_ID": user_id},
            {"$set": update_fields}
        )
        logger.info(f"User details updated for user {user_id}.")
        return True
    except Exception as e:
        logger.error(f"Error updating user details for user {user_id}: {e}")
        return False


async def get_user_details(user_id: int) -> dict | None:
    """
    Возвращает детали пользователя по заданному идентификатору.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - dict: Словарь с деталями пользователя, если пользователь найден.
    - None, если пользователь не найден или произошла ошибка.
    """
    logger.debug("def get_user_details")
    try:
        user = await users_collection.find_one({"USER_ID": user_id})
        if user:
            logger.info(f"User details retrieved for user {user_id}.")
            return user
        else:
            logger.info(f"User {user_id} not found in database.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving user details for user {user_id}: {e}")
        return None


async def update_language_in_db(user_id: int, language: str) -> bool:
    """
    Обновляет язык пользователя в базе данных.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.
    - language (str): Новый язык пользователя.

    Возвращает:
    - True, если обновление прошло успешно.
    - False, если обновление не удалось.
    """
    logger.debug("def update_language_in_db")
    try:
        await users_collection.update_one(
            {"USER_ID": user_id},
            {"$set": {"LANGUAGE": language}}
        )
        logger.info(f"Language updated to {language} for user {user_id}.")
        return True
    except Exception as e:
        logger.error(f"Error updating language for user {user_id}: {e}")
        return False


async def add_user_to_db(user_id: int) -> bool:
    """
    Добавляет нового пользователя в базу данных с заданным идентификатором.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - True, если добавление прошло успешно.
    - False, если добавление не удалось.
    """
    logger.debug("def add_user_to_db")
    try:
        user_data = {
            "USER_ID": user_id,
            "ADDR": None,
            "REF_BY_USER": None,
            "TWITTER_USER": None,
            "LANGUAGE": "ENG",
            "NUM_OF_REFS": 0,
            "REF_POINTS": 0,
            "POINTS": 0,
            "TASKS_DONE": [],
            "TASKS_AWAIT": [],
            "STATE": "RegistrationState.lang_choose_state"
        }
        await users_collection.insert_one(user_data)
        logger.info(f"User {user_id} added to database with default values.")
        return True
    except Exception as e:
        logger.error(f"Error adding user {user_id} to database: {e}")
        return False


async def get_language_for_user(user_id: int) -> str | None:
    """
    Возвращает язык пользователя по заданному идентификатору.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - str: Язык пользователя, если он найден.
    - None, если пользователь не найден или произошла ошибка.
    """
    logger.debug("def get_language_for_user")
    try:
        user = await users_collection.find_one({"USER_ID": user_id}, {"LANGUAGE": 1, "_id": 0})
        if user and "LANGUAGE" in user:
            logger.info(f"Language for user {user_id} is {user['LANGUAGE']}.")
            return user["LANGUAGE"]
        else:
            logger.info(f"Language for user {user_id} not found. Defaulting to 'ENG'.")
            return "ENG"
    except Exception as e:
        logger.error(f"Error retrieving language for user {user_id}: {e}")
        return None


async def add_referrer_to_user(user_id: int, referrer_id: int) -> bool:
    """
    Добавляет идентификатор пользователя-реферера к записи пользователя.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.
    - referrer_id (int): Уникальный идентификатор пользователя-реферера.

    Возвращает:
    - True, если обновление прошло успешно.
    - False, если обновление не удалось.
    """
    logger.debug("def add_referrer_to_user")
    try:
        await users_collection.update_one(
            {"USER_ID": user_id},
            {"$set": {"REF_BY_USER": referrer_id}}
        )
        logger.info(f"Referrer {referrer_id} added to user {user_id}.")
        return True
    except Exception as e:
        logger.error(f"Error adding referrer to user {user_id}: {e}")
        return False


async def increment_referrer_count(referrer_id: int) -> None:
    """
    Увеличивает количество рефералов и количество очков за рефералов у пользователя-реферера в MongoDB.

    Параметры:
    - referrer_id (int): Уникальный идентификатор пользователя-реферера.
    """
    logger.debug("def increment_refferer_count")
    try:
        user = await users_collection.find_one({"USER_ID": referrer_id})
        if user:
            current_ref_count = user.get("NUM_OF_REFS", 0)
            current_ref_points = user.get("REF_POINTS", 0)
            new_ref_count = current_ref_count + 1
            new_ref_points = current_ref_points + REFERRAL_REWARD
            await users_collection.update_one(
                {"USER_ID": referrer_id},
                {"$set": {"NUM_OF_REFS": new_ref_count, "REF_POINTS": new_ref_points}}
            )
            logger.info(f"Referral count for user {referrer_id} incremented to {new_ref_count}.")
            logger.info(f"Referral points for user {referrer_id} incremented to {new_ref_points}.")
        else:
            logger.warning(f"User {referrer_id} not found in database.")
    except Exception as e:
        logger.error(f"Error incrementing referral count or points for user {referrer_id}: {e}")


async def decrement_referrer_count(referrer_id: int) -> None:
    """
    Уменьшает количество рефералов и количество очков за рефералов у пользователя-реферера в MongoDB.

    Параметры:
    - referrer_id (int): Уникальный идентификатор пользователя-реферера.
    """
    logger.debug("def decrement_referrer_count")
    try:
        user = await users_collection.find_one({"USER_ID": referrer_id})
        if user:
            current_ref_count = user.get("NUM_OF_REFS", 0)
            current_ref_points = user.get("REF_POINTS", 0)
            new_ref_count = max(0, current_ref_count - 1)
            new_ref_points = max(0, current_ref_points - REFERRAL_REWARD)
            await users_collection.update_one(
                {"USER_ID": referrer_id},
                {"$set": {"NUM_OF_REFS": new_ref_count, "REF_POINTS": new_ref_points}}
            )
            logger.info(f"Referral count for user {referrer_id} decremented to {new_ref_count}.")
            logger.info(f"Referral points for user {referrer_id} decremented to {new_ref_points}.")
        else:
            logger.warning(f"User {referrer_id} not found in database.")
    except Exception as e:
        logger.error(f"Error decrementing referral count or points for user {referrer_id}: {e}")


async def get_referrer(user_id: int) -> int | None:
    """
    Возвращает идентификатор реферера для указанного пользователя.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - referrer_id (int): Идентификатор пользователя-реферера, если он существует.
    - None, если реферер не найден или произошла ошибка.
    """
    logger.debug("def get_referrer")
    try:
        user = await users_collection.find_one({"USER_ID": user_id})
        if user:
            return user.get("REF_BY_USER")
        else:
            logger.info(f"Referrer not found for user {user_id}")
            return None
    except Exception as e:
        logger.error(f"Error retrieving referrer for user {user_id}: {e}")
        return None


async def check_wallet_exists(wallet_address: str) -> bool:
    """
    Проверяет, отсутствует ли запись с указанным кошельком в MongoDB.

    Параметры:
    - wallet_address (str): Адрес кошелька для проверки.

    Возвращает:
    - True, если запись с указанным кошельком отсутствует в MongoDB.
    - False, если запись с указанным кошельком найдена в MongoDB.
    """
    logger.debug("def check_wallet_exists")
    try:
        result = await users_collection.find_one({"ADDR": wallet_address})
        return result is None
    except Exception as e:
        logger.error(f"Error checking wallet address in MongoDB: {e}")
        return False


async def mark_task_as_done(user_id: int, task_index: int) -> bool:
    """
    Добавляет индекс выполненного задания в список выполненных заданий пользователя в MongoDB.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.
    - task_index (int): Индекс выполненного задания.

    Возвращает:
    - True, если обновление прошло успешно.
    - False, если в процессе обновления произошла ошибка.
    """
    logger.debug("def mark_task_as_done")
    try:
        result = await users_collection.update_one(
            {"USER_ID": user_id},
            {"$addToSet": {"TASKS_DONE": task_index}}
        )
        if result.modified_count > 0:
            logger.debug(f"Task {task_index} marked as done for user {user_id}.")
            return True
        else:
            logger.debug(f"Task {task_index} was already marked as done or user {user_id} not found.")
            return False
    except Exception as e:
        logger.error(f"Error marking task {task_index} as done for user {user_id}: {e}")
        return False


async def mark_task_as_await(user_id: int, task_index: int) -> bool:
    """
    Добавляет индекс выполненного задания в список выполненных заданий пользователя в MongoDB.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.
    - task_index (int): Индекс выполненного задания.

    Возвращает:
    - True, если обновление прошло успешно.
    - False, если в процессе обновления произошла ошибка.
    """
    logger.debug("def mark_task_as_await")
    try:
        result = await users_collection.update_one(
            {"USER_ID": user_id},
            {"$addToSet": {"TASKS_AWAIT": task_index}}
        )
        if result.modified_count > 0:
            logger.debug(f"Task {task_index} marked as await for user {user_id}.")
            return True
        else:
            logger.debug(f"Task {task_index} was already marked as await or user {user_id} not found.")
            return False
    except Exception as e:
        logger.error(f"Error marking task {task_index} as await for user {user_id}: {e}")
        return False


async def remove_task_from_await(user_id: int, task_index: int) -> bool:
    """
    Removes the index of the pending task from the user's pending tasks list in MongoDB.
    Returns:
    - True if the update was successful.
    - False if there was an error during the update.
    """
    logger.debug("def remove_task_from_await")
    try:
        result = await users_collection.update_one(
            {"USER_ID": user_id},
            {"$pull": {"TASKS_AWAIT": task_index}}
        )
        if result.modified_count > 0:
            logger.debug(f"Task {task_index} removed from pending tasks for user {user_id}.")
            return True
        else:
            logger.debug(f"Task {task_index} was not found in pending tasks or user {user_id} not found.")
            return False
    except Exception as e:
        logger.error(f"Error removing task {task_index} from pending tasks for user {user_id}: {e}")
        return False


async def add_points_to_user(user_id: int, points: int) -> bool:
    """
    Добавляет указанное количество очков к POINTS пользователя в базе данных.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.
    - points (int): Количество очков для добавления.

    Возвращает:
    - True, если обновление прошло успешно.
    - False, если в процессе обновления произошла ошибка.
    """
    logger.debug("def add_points_to_user")
    try:
        result = await users_collection.update_one(
            {"USER_ID": user_id},
            {"$inc": {"POINTS": points}}
        )
        if result.modified_count > 0:
            logger.debug(f"Added {points} points to user {user_id}.")
            return True
        else:
            logger.debug(f"User {user_id} not found or no points added.")
            return False
    except Exception as e:
        logger.error(f"Error adding points to user {user_id}: {e}")
        return False


async def set_user_state(user_id: int, state: str):
    """
    Set the user's state in the database.

    Parameters:
    - user_id (int): The user's unique identifier.
    - state (str): The state to set for the user.
    - state_context (FSMContext): The FSM context to manipulate state data.
    """
    try:
        await users_collection.update_one(
            {"USER_ID": user_id},
            {"$set": {"STATE": state}},
            upsert=True
        )
        logger.debug(f"User {user_id} state set to {state}.")
    except Exception as e:
        logger.error(f"Error setting state for user {user_id}: {e}")


async def get_state_for_user(user_id: int) -> str | None:
    """
    Returns the state of a user by the given user identifier.

    Parameters:
    - user_id (int): The unique identifier of the user.

    Returns:
    - str: The state of the user if found.
    - None, if the user is not found or an error occurred.
    """
    logger.debug("def get_state_for_user")
    try:
        user = await users_collection.find_one({"USER_ID": user_id}, {"STATE": 1, "_id": 0})
        if user and "STATE" in user:
            logger.debug(f"State for user {user_id} is {user['STATE']}.")
            return await get_state_from_string(user["STATE"])
        else:
            logger.debug(f"State for user {user_id} not found.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving state for user {user_id}: {e}")
        return None


async def get_all_users() -> list:
    """
    Получает всех пользователей из коллекции `users_collection`.

    Функция выполняет запрос ко всем документам в коллекции `users_collection`,
    преобразует их в список и возвращает его.

    Возвращает:
    - list: Список всех пользователей, содержащих документы с данными пользователей.
    """
    logger.debug("Запрос всех пользователей из базы данных.")
    try:
        users_cursor = users_collection.find()
        users_list = await users_cursor.to_list(length=None)
        logger.debug(f"Получено {len(users_list)} пользователей из базы данных.")
        return users_list
    except Exception as e:
        logger.error(f"Ошибка при получении всех пользователей: {e}")
        return []


async def add_admin(admin_id: int) -> None:
    """
    Добавляет администратора в коллекцию `admins_collection`.

    Функция выполняет обновление или вставку документа с идентификатором администратора в коллекцию `admins_collection`.
    После этого обновляет глобальный список идентификаторов администраторов.

    Параметры:
    - admin_id (int): Идентификатор администратора, который нужно добавить.
    """
    try:
        logger.debug(f"Добавление администратора с ID {admin_id}.")
        await admins_collection.update_one({"_id": admin_id}, {"$set": {"_id": admin_id}}, upsert=True)
        await update_admins_ids()
        logger.debug(f"Администратор с ID {admin_id} успешно добавлен и список администраторов обновлен.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении администратора с ID {admin_id}: {e}")


async def remove_admin(admin_id: int) -> None:
    """
    Удаляет администратора из коллекции `admins_collection`.

    Функция выполняет удаление документа с идентификатором администратора из коллекции `admins_collection`.
    После этого обновляет глобальный список идентификаторов администраторов.

    Параметры:
    - admin_id (int): Идентификатор администратора, который нужно удалить.
    """
    try:
        logger.debug(f"Удаление администратора с ID {admin_id}.")
        await admins_collection.delete_one({"_id": admin_id})
        await update_admins_ids()
        logger.debug(f"Администратор с ID {admin_id} успешно удален и список администраторов обновлен.")
    except Exception as e:
        logger.error(f"Ошибка при удалении администратора с ID {admin_id}: {e}")


async def get_top_users() -> list:
    """
    Возвращает топ 20 пользователей по количеству очков (сумма POINTS и REF_POINTS).

    Возвращает:
    - list: Список из топ 20 пользователей, где каждый элемент - это список [user_id, points].
    """
    try:
        # Запрос к базе данных для получения пользователей, отсортированных по сумме POINTS и REF_POINTS
        cursor = users_collection.aggregate([
            {
                "$project": {
                    "USER_ID": 1,
                    "total_points": {"$add": ["$POINTS", "$REF_POINTS"]}
                }
            },
            {"$sort": {"total_points": DESCENDING}},
            {"$limit": 20}
        ])

        top_users = await cursor.to_list(length=15)

        # Формирование списка с user_id и их общими очками
        top_users_list = [[user["USER_ID"], user["total_points"]] for user in top_users]

        return top_users_list
    except Exception as e:
        logger.error(f"Error retrieving top users: {e}")
        return []


async def format_top_users(top_users):
    """
    Форматирует список топ пользователей в строку с нумерацией и указанием ID и Points.

    Параметры:
    - top_users (list): Список топ пользователей в формате [["ID", points], ["ID", points], ...]

    Возвращает:
    - str: Форматированная строка с нумерацией и указанием ID и Points.
    """
    formatted_output = []
    for index, user in enumerate(top_users, start=1):
        formatted_output.append(f"{index}. ID {user[0]} - Points {user[1]}")

    return "\n".join(formatted_output)


async def get_user_address(user_id: int) -> str | None:
    """
    Возвращает адрес пользователя по указанному юзер айди.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - address (str): Адрес пользователя, если он существует.
    - None, если пользователь не найден или произошла ошибка.
    """
    logger.debug("def get_user_address")
    try:
        user = await users_collection.find_one({"USER_ID": user_id})
        if user:
            return user.get("ADDR")
        else:
            logger.info(f"User not found for user_id {user_id}")
            return None
    except Exception as e:
        logger.error(f"Error retrieving user address for user_id {user_id}: {e}")
        return None
