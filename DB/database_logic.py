import motor.motor_asyncio
from bson.objectid import ObjectId
from settings.config import REFERRAL_REWARD
from DB.mongo import users_collection


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


# Функция получения данных пользователя
# async def get_user_details(user_id: int) -> dict | None:
#     """
#     Возвращает детали пользователя по заданному идентификатору.
#
#     Параметры:
#     - user_id (int): Уникальный идентификатор пользователя.
#
#     Возвращает:
#     - dict: Словарь с деталями пользователя, если пользователь найден.
#     - None, если пользователь не найден или произошла ошибка.
#     """
#     try:
#         user = await users_collection.find_one({"USER_ID": user_id})
#         if user:
#             print(f"User details retrieved for user {user_id}.")
#             return user
#         else:
#             print(f"User {user_id} not found in database.")
#             return None
#     except Exception as e:
#         print(f"Error retrieving user details for user {user_id}: {e}")
#         return None

async def get_user_details(user_id: int) -> dict:
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
        }
        await users_collection.insert_one(user_data)
        print(f"User {user_id} added to database with default values.")
        return True
    except Exception as e:
        print(f"Error adding user {user_id} to database: {e}")
        return False


async def get_language_for_user(user_id: int) -> str:
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
            return None
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
async def get_referrer(user_id: int) -> int:
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
