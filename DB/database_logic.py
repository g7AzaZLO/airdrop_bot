from logic.admins import update_admins_ids
from settings.config import REFERRAL_REWARD, tasks_init
from DB.mongo import users_collection, tasks_collection, admin_messages_collection, admins_collection
from FSM.states import get_state_from_string


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


async def insert_tasks() -> None:
    """
    Вставляет задачи в коллекцию `tasks_collection` в базе данных MongoDB.

    Функция перебирает все задачи из словаря `tasks_init`, добавляет каждому
    из них идентификатор `_id` и вставляет их в коллекцию `tasks_collection`
    """
    for task_id, task_data in tasks_init.items():
        task_data["_id"] = task_id
        await tasks_collection.update_one({"_id": task_id}, {"$set": task_data}, upsert=True)


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
    user_doc = await admin_messages_collection.find_one({"user_id": user_id})
    if not user_doc:
        return {}
    admin_messages_dict = {task["_id"]: task for task in user_doc.get("tasks", [])}
    return admin_messages_dict


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
    user_doc = await admin_messages_collection.find_one({"user_id": user_id})
    if not user_doc:
        return
    updated_tasks = [task for task in user_doc.get("tasks", []) if task["_id"] != task_id]
    if updated_tasks:
        await admin_messages_collection.update_one(
            {"user_id": user_id},
            {"$set": {"tasks": updated_tasks}}
        )
    else:
        await admin_messages_collection.delete_one({"user_id": user_id})


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
    user_doc = await admin_messages_collection.find_one({"user_id": user_id})
    if user_doc is None:
        user_doc = {"user_id": user_id, "tasks": []}
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
                break
        if not task_exists:
            user_doc["tasks"].append(message_data)
    await admin_messages_collection.update_one(
        {"user_id": user_id},
        {"$set": {"tasks": user_doc["tasks"]}},
        upsert=True
    )


async def get_all_tasks() -> dict:
    """
    Получает все задачи из коллекции `tasks_collection` и возвращает их в виде словаря.

    Функция выполняет запрос ко всем документам в коллекции `tasks_collection`, преобразует их в список,
    а затем в словарь, где ключами являются идентификаторы задач (`_id`), а значениями - данные задач.

    Возвращает:
    - dict: Словарь, содержащий все задачи, где ключами являются идентификаторы задач, а значениями - данные задач.
      """
    tasks_cursor = tasks_collection.find()
    tasks_list = await tasks_cursor.to_list(length=None)
    tasks_dict = {task["_id"]: task for task in tasks_list}
    return tasks_dict


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
    """
    Получает всех пользователей из коллекции `users_collection`.

    Функция выполняет запрос ко всем документам в коллекции `users_collection`,
    преобразует их в список и возвращает его.

    Возвращает:
    - list: Список всех пользователей, содержащих документы с данными пользователей.
    """
    users_cursor = users_collection.find()
    users_list = await users_cursor.to_list(length=None)
    return users_list


async def add_admin(admin_id: int) -> None:
    """
    Добавляет администратора в коллекцию `admins_collection`.

    Функция выполняет обновление или вставку документа с идентификатором администратора в коллекцию `admins_collection`.
    После этого обновляет глобальный список идентификаторов администраторов.

    Параметры:
    - admin_id (int): Идентификатор администратора, который нужно добавить.
    """
    await admins_collection.update_one({"_id": admin_id}, {"$set": {"_id": admin_id}}, upsert=True)
    await update_admins_ids()


async def remove_admin(admin_id: int) -> None:
    """
    Удаляет администратора из коллекции `admins_collection`.

    Функция выполняет удаление документа с идентификатором администратора из коллекции `admins_collection`.
    После этого обновляет глобальный список идентификаторов администраторов.

    Параметры:
    - admin_id (int): Идентификатор администратора, который нужно удалить.
    """
    await admins_collection.delete_one({"_id": admin_id})
    await update_admins_ids()
