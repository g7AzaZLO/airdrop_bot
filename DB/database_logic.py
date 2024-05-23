from logic.admins import update_admins_ids
from settings.config import REFERRAL_REWARD, tasks_init
from DB.mongo import users_collection, tasks_collection, admin_messages_collection, admins_collection
from FSM.states import get_state_from_string


# Функция инициализации базы данных
async def initialize_db() -> None:
    """
    Инициализирует коллекцию пользователей в MongoDB.
    Создает индексы для уникальности и быстрого доступа к полям, таким как USER_ID.
    Если база данных уже существует, выводит соответствующее сообщение.
    """
    try:
        existing_indexes = await users_collection.index_information()
        if 'USER_ID_1' in existing_indexes:
            print("Database already initialized with required indexes.")
        else:
            await users_collection.create_index("USER_ID", unique=True)

            print("Database initialized successfully with indexes on USER_ID")
    except Exception as e:
        print(f"Error initializing database: {e}")


async def insert_tasks():
    for task_id, task_data in tasks_init.items():
        task_data["_id"] = task_id
        await tasks_collection.update_one({"_id": task_id}, {"$set": task_data}, upsert=True)


async def delete_admin_message(task_id: int):
    await admin_messages_collection.delete_one({"_id": task_id})


async def get_admin_messages_dict():
    admin_messages_cursor = admin_messages_collection.find()
    admin_messages_list = await admin_messages_cursor.to_list(length=None)  # Преобразуем курсор в список
    admin_messages_dict = {message["_id"]: message for message in admin_messages_list}
    return admin_messages_dict


async def insert_admin_messages(admin_messages: dict) -> None:
    for task_id, message_data in admin_messages.items():
        message_data["_id"] = task_id
        # Преобразуем ключи в строки
        message_data = {str(k): v for k, v in message_data.items()}
        await admin_messages_collection.update_one({"_id": task_id}, {"$set": message_data}, upsert=True)


async def get_all_tasks():
    tasks_cursor = tasks_collection.find()
    tasks_list = await tasks_cursor.to_list(length=None)  # Преобразуем курсор в список
    tasks_dict = {task["_id"]: task for task in tasks_list}
    return tasks_dict


# Функция удаления пользователя из базы данных
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
            print(f"User {user_id} deleted successfully.")
            return True
        else:
            print(f"User {user_id} not found in database.")
            return False
    except Exception as e:
        print(f"Error deleting user {user_id} from database: {e}")
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
        print(f"Error checking if user {user_id} is already in database: {e}")
        return False


# Функция обновления данных пользователя
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
    print("def update_user_details")
    try:
        update_fields = {key: value for key, value in kwargs.items()}
        await users_collection.update_one(
            {"USER_ID": user_id},
            {"$set": update_fields}
        )
        print(f"User details updated for user {user_id}.")
        return True
    except Exception as e:
        print(f"Error updating user details: {e}")
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
    print("def get_user_details")
    try:
        user = await users_collection.find_one({"USER_ID": user_id})
        if user:
            print(f"User details retrieved for user {user_id}.")
            return user
        else:
            print(f"User {user_id} not found in database.")
            return None
    except Exception as e:
        print(f"Error retrieving user details for user {user_id}: {e}")
        return None


# Функция обновления языка пользователя
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
    print("def update_language_in_db")
    try:
        await users_collection.update_one(
            {"USER_ID": user_id},
            {"$set": {"LANGUAGE": language}}
        )
        print(f"Language updated to {language} for user {user_id}.")
        return True
    except Exception as e:
        print(f"Error updating language for user {user_id}: {e}")
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
    print("def add_user_to_db")
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
        print(f"User {user_id} added to database with default values.")
        return True
    except Exception as e:
        print(f"Error adding user {user_id} to database: {e}")
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
    print("def get_language_for_user")
    try:
        user = await users_collection.find_one({"USER_ID": user_id}, {"LANGUAGE": 1, "_id": 0})
        if user and "LANGUAGE" in user:
            print(f"Language for user {user_id} is {user['LANGUAGE']}.")
            return user["LANGUAGE"]
        else:
            print(f"Language for user {user_id} not found.")
            return "ENG"
    except Exception as e:
        print(f"Error retrieving language for user {user_id}: {e}")
        return None


# Функция добавления реферера к пользователю
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
    print("def add_referrer_to_user")
    try:
        await users_collection.update_one(
            {"USER_ID": user_id},
            {"$set": {"REF_BY_USER": referrer_id}}
        )
        print(f"Referrer {referrer_id} added to user {user_id}.")
        return True
    except Exception as e:
        print(f"Error adding referrer to user {user_id}: {e}")
        return False


# Функция увеличения реферального счетчика и очков
async def increment_referrer_count(referrer_id: int) -> None:
    """
    Увеличивает количество рефералов и количество очков за рефералов у пользователя-реферера в MongoDB.

    Параметры:
    - referrer_id (int): Уникальный идентификатор пользователя-реферера.
    """
    print("def increment_refferer_count")
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
            print(f"Referral count for user {referrer_id} incremented to {new_ref_count}.")
            print(f"Referral points for user {referrer_id} incremented to {new_ref_points}.")
        else:
            print(f"User {referrer_id} not found in database.")
    except Exception as e:
        print(f"Error incrementing referral count or points for user {referrer_id}: {e}")


async def decrement_referrer_count(referrer_id: int) -> None:
    """
    Уменьшает количество рефералов и количество очков за рефералов у пользователя-реферера в MongoDB.

    Параметры:
    - referrer_id (int): Уникальный идентификатор пользователя-реферера.
    """
    print("def decrement_refferer_count")
    try:
        user = await users_collection.find_one({"USER_ID": referrer_id})
        if user:
            current_ref_count = user.get("NUM_OF_REFS", 0)
            current_ref_points = user.get("REF_POINTS", 0)
            new_ref_count = max(0, current_ref_count - 1)  # Убедимся, что количество рефералов не отрицательное
            new_ref_points = max(0, current_ref_points - REFERRAL_REWARD)  # Убедимся, что очки не отрицательные
            await users_collection.update_one(
                {"USER_ID": referrer_id},
                {"$set": {"NUM_OF_REFS": new_ref_count, "REF_POINTS": new_ref_points}}
            )
            print(f"Referral count for user {referrer_id} decremented to {new_ref_count}.")
            print(f"Referral points for user {referrer_id} decremented to {new_ref_points}.")
        else:
            print(f"User {referrer_id} not found in database.")
    except Exception as e:
        print(f"Error decrementing referral count or points for user {referrer_id}: {e}")


# Функция получения реферера
async def get_referrer(user_id: int) -> int | None:
    """
    Возвращает идентификатор реферера для указанного пользователя.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - referrer_id (int): Идентификатор пользователя-реферера, если он существует.
    - None, если реферер не найден или произошла ошибка.
    """
    try:
        user = await users_collection.find_one({"USER_ID": user_id})
        if user:
            return user.get("REF_BY_USER")
        else:
            return None
    except Exception as e:
        print(f"Error retrieving referrer for user {user_id}: {e}")
        return None


# Функция проверки наличия кошелька
async def check_wallet_exists(wallet_address: str) -> bool:
    """
    Проверяет, отсутствует ли запись с указанным кошельком в MongoDB.

    Параметры:
    - wallet_address (str): Адрес кошелька для проверки.

    Возвращает:
    - True, если запись с указанным кошельком отсутствует в MongoDB.
    - False, если запись с указанным кошельком найдена в MongoDB.
    """
    try:
        result = await users_collection.find_one({"ADDR": wallet_address})
        return result is None
    except Exception as e:
        print(f"Error checking wallet address in MongoDB: {e}")
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
    try:
        result = await users_collection.update_one(
            {"USER_ID": user_id},
            {"$addToSet": {"TASKS_DONE": task_index}}
        )
        if result.modified_count > 0:
            print(f"Task {task_index} marked as done for user {user_id}.")
            return True
        else:
            print(f"Task {task_index} was already marked as done or user {user_id} not found.")
            return False
    except Exception as e:
        print(f"Error marking task {task_index} as done for user {user_id}: {e}")
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
    try:
        result = await users_collection.update_one(
            {"USER_ID": user_id},
            {"$addToSet": {"TASKS_AWAIT": task_index}}
        )
        if result.modified_count > 0:
            print(f"Task {task_index} marked as await for user {user_id}.")
            return True
        else:
            print(f"Task {task_index} was already marked as await or user {user_id} not found.")
            return False
    except Exception as e:
        print(f"Error marking task {task_index} as await for user {user_id}: {e}")
        return False


async def remove_task_from_await(user_id: int, task_index: int) -> bool:
    """
    Removes the index of the pending task from the user's pending tasks list in MongoDB.
    Returns:
    - True if the update was successful.
    - False if there was an error during the update.
    """
    try:
        result = await users_collection.update_one(
            {"USER_ID": user_id},
            {"$pull": {"TASKS_AWAIT": task_index}}
        )
        if result.modified_count > 0:
            print(f"Task {task_index} removed from pending tasks for user {user_id}.")
            return True
        else:
            print(f"Task {task_index} was not found in pending tasks or user {user_id} not found.")
            return False
    except Exception as e:
        print(f"Error removing task {task_index} from pending tasks for user {user_id}: {e}")
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
    try:
        result = await users_collection.update_one(
            {"USER_ID": user_id},
            {"$inc": {"POINTS": points}}
        )
        if result.modified_count > 0:
            print(f"Added {points} points to user {user_id}.")
            return True
        else:
            print(f"User {user_id} not found or no points added.")
            return False
    except Exception as e:
        print(f"Error adding points to user {user_id}: {e}")
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
        # Additionally, save or update the state in the MongoDB
        await users_collection.update_one(
            {"USER_ID": user_id},
            {"$set": {"STATE": state}},
            upsert=True
        )
    except Exception as e:
        print(f"Error setting state for user {user_id}: {e}")


async def get_state_for_user(user_id: int) -> str | None:
    """
    Returns the state of a user by the given user identifier.

    Parameters:
    - user_id (int): The unique identifier of the user.

    Returns:
    - str: The state of the user if found.
    - None, if the user is not found or an error occurred.
    """
    print("def get_state_for_user")
    try:
        user = await users_collection.find_one({"USER_ID": user_id}, {"STATE": 1, "_id": 0})
        if user and "STATE" in user:
            print(f"State for user {user_id} is {user['STATE']}.")
            return await get_state_from_string(user["STATE"])
        else:
            print(f"State for user {user_id} not found.")
            return None
    except Exception as e:
        print(f"Error retrieving state for user {user_id}: {e}")
        return None


async def get_all_users() -> list:
    users_cursor = users_collection.find()
    users_list = await users_cursor.to_list(length=None)
    return users_list


# Функция для добавления администратора
async def add_admin(admin_id: int) -> None:
    await admins_collection.update_one({"_id": admin_id}, {"$set": {"_id": admin_id}}, upsert=True)
    await update_admins_ids()


# Функция для удаления администратора
async def remove_admin(admin_id: int) -> None:
    await admins_collection.delete_one({"_id": admin_id})
    await update_admins_ids()
