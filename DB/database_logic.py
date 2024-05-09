import sqlite3
from settings.config import DATABASE_FILE, REFERRAL_REWARD
from os.path import isfile


async def initialize_db() -> None:
    """
    Инициализирует базу данных. Проверяет наличие файла базы данных.
    Если файл не существует, создает базу данных и таблицу faucetClaims.

    В таблице faucetClaims предусмотрены следующие поля:
    - USER_ID (INTEGER): уникальный идентификатор пользователя,
    - ADDR (TEXT): адрес пользователя,
    - ALREADY_REG (BOOL) - зарегестрирован ли пользователь.
    - NUM_OF_REFS (INT) - количество рефералов
    - REF_BY_USER (INTEGER) - user_id пользователя чьим рефералом является
    - TWITTER_USER (TEXT) - ссылка на твиттер пользователя
    - LANGUAGE (TEXT) - язык пользователя
    - REF_POINTS (INT)
    - POINTS (INT)

    Печатает соответствующее сообщение о наличии или создании базы данных.
    """
    if isfile(DATABASE_FILE):
        print("Database exists...")
    else:
        print("Creating Database...")
        execute_non_query(
            "CREATE TABLE users (USER_ID INTEGER, ADDR TEXT, ALREADY_REG BOOL, NUM_OF_REFS INT, REF_BY_USER INTEGER, TWITTER_USER TEXT, LANGUAGE TEXT, REF_POINTS INT, POINTS INT);")
        print("Database created successfully")


def execute_non_query(command: str) -> None:
    """
    Выполняет SQL-команду, не возвращающую данные (например, INSERT, UPDATE, DELETE, CREATE).

    Параметры:
    - command (str): SQL-команда для выполнения.

    Открывает соединение с базой данных, указанной в переменной DATABASE_FILE, выполняет команду,
    фиксирует изменения и закрывает соединение
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute(command)
    conn.commit()
    conn.close()


async def delete_user_from_db(user_id: int) -> bool:
    """
    Удаляет пользователя из таблицы базы данных по заданному идентификатору пользователя.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя для удаления.

    Возвращает:
    - True, если удаление прошло успешно.
    - False, если в процессе удаления произошла ошибка.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE USER_ID = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


async def check_is_user_already_here(user_id: int) -> bool:
    """
    Проверяет, существует ли пользователь с заданным идентификатором в таблице 'users' базы данных.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя для проверки.

    Возвращает:
    - True, если пользователя с таким идентификатором нет в базе данных.
    - False, если пользователь с таким идентификатором уже есть в базе данных.

    Функция использует параметризованный запрос для предотвращения SQL-инъекций, устанавливает
    соединение с базой данных, выполняет SQL-запрос для поиска пользователя с указанным идентификатором
    и возвращает результат на основе наличия или отсутствия данных в ответе.
    """
    print("def check_is_user_already_here")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE USER_ID = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return not (len(rows) == 0)
    except Exception as e:
        print(e)
        return False


async def register_user(user_id: int, addr: str, twitter_user: str, language: str):
    """
    Registers a new user in the database with initial details such as address, Twitter handle, and language preference.

    Parameters:
    - user_id (int): Unique identifier for the user.
    - addr (str): Address of the user.
    - twitter_user (str): Twitter handle of the user.
    - language (str): Preferred language of the user.

    Returns:
    - True if the user is successfully registered.
    - False if the registration fails.

    The function opens a connection to the database, executes an INSERT query to add the new user with the given details into the users table, and commits the transaction. It returns the success status of the registration.
    """
    print("def register_user")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (USER_ID, ADDR, ALREADY_REG, NUM_OF_REFS, TWITTER_USER, LANGUAGE) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, addr, True, 0, twitter_user, language))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


async def update_user_details(user_id: int, **kwargs) -> bool:
    """
    Updates specific user details in the database. Accepts the user ID and keyword arguments representing the fields to update.

    Parameters:
    - user_id (int): Unique identifier of the user.
    - **kwargs: Variable keyword arguments representing column-value pairs to be updated in the database.

    Returns:
    - True if the update is successful.
    - False if the update fails.

    The function uses parameterized queries to prevent SQL injections, opens a connection to the database, executes the SQL command to update specific fields for a given user ID, and returns the success status of the operation.
    """
    print("def update_user_details")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        for key, value in kwargs.items():
            cursor.execute(f"UPDATE users SET {key} = ? WHERE USER_ID = ?", (value, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


async def get_user_details(user_id: int):
    """
    Retrieves all stored details for a specific user from the database.

    Parameters:
    - user_id (int): Unique identifier of the user to retrieve details for.

    Returns:
    - A tuple containing the user details if the user exists in the database.
    - None if there is no such user or if an error occurs.

    The function establishes a connection to the database, executes a SELECT query to fetch all columns for the specified user ID, and returns the result or None based on the presence of data.
    """
    print("def get_user_details")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE USER_ID = ?", (user_id,))
        user_details = cursor.fetchone()
        conn.close()
        return user_details
    except Exception as e:
        print(e)
        return None


async def list_users_by_filter(**filters):
    """
    Fetches a list of users who match specified filter criteria from the database.

    Parameters:
    - **filters: Variable keyword arguments where each key-value pair represents a column and a corresponding filter value to apply.

    Returns:
    - A list of tuples, where each tuple represents a user record that matches the criteria.
    - An empty list if no users meet the criteria or in case of an error.

    The function constructs a SQL query dynamically based on the provided filters, uses parameterized queries to safely include values, and retrieves users from the database. It returns a list of users or an empty list depending on query results.
    """
    print("def list_users_by_filter")
    query = "SELECT * FROM users"
    conditions = []
    params = []
    for key, value in filters.items():
        conditions.append(f"{key} = ?")
        params.append(value)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(e)
        return []


async def update_language_in_db(user_id: int, language: str) -> None:
    """
    Обновляет или добавляет язык пользователя в базе данных.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.
    - language (str): Выбранный язык пользователя.
    """
    print("def update_language_in_db")
    try:
        # Формирование SQL команды для обновления языка пользователя
        command = f"UPDATE users SET LANGUAGE = '{language}' WHERE USER_ID = {user_id};"
        execute_non_query(command)
        print("Language updated successfully.")
    except Exception as e:
        print(f"Error updating language in DB: {e}")


async def add_user_to_db(user_id: int) -> None:
    """
    Добавляет нового пользователя в базу данных.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.
    """
    try:
        command = f"INSERT INTO users (USER_ID) VALUES ({user_id})"
        execute_non_query(command)
        print(f"User {user_id} added to the database.")
    except Exception as e:
        print(f"Error adding user {user_id} to the database: {e}")


async def get_language_for_user(user_id: int) -> str:
    """
    Получает язык пользователя из базы данных.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - language (str): Язык пользователя, хранящийся в базе данных. Возвращает None, если не найдено.
    """
    conn = sqlite3.connect(DATABASE_FILE)  # Adjust database connection as necessary
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT LANGUAGE FROM users WHERE USER_ID = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the language if available
        else:
            return None  # No language set
    except Exception as e:
        print(f"Error fetching language from DB: {e}")
        return None
    finally:
        conn.close()


async def add_referrer_to_user(user_id: int, referrer_id: int) -> None:
    """
    Добавляет идентификатор пользователя-реферера к записи пользователя.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET REF_BY_USER = ? WHERE USER_ID = ?", (referrer_id, user_id))
        conn.commit()
        print(f"Referrer {referrer_id} added to user {user_id}.")
    except Exception as e:
        print(f"Error adding referrer to user {user_id}: {e}")
    finally:
        conn.close()


async def increment_referrer_count(referrer_id: int) -> None:
    """
    Увеличивает количество рефералов и количество очков за рефералов у пользователя-реферера.

    Параметры:
    - referrer_id (int): Уникальный идентификатор пользователя-реферера.

    Эта функция обновляет запись в таблице `users`, увеличивая счетчик рефералов и очки за рефералов
    для указанного пользователя.
    """
    print("def increment_refferer_count")
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Получаем текущее количество рефералов и очков за рефералов
        cursor.execute("SELECT NUM_OF_REFS, REF_POINTS FROM users WHERE USER_ID = ?", (referrer_id,))
        result = cursor.fetchone()
        if result:
            current_ref_count = result[0] if result[0] is not None else 0
            current_ref_points = result[1] if result[1] is not None else 0
        else:
            current_ref_count = 0
            current_ref_points = 0

        # Увеличиваем количество рефералов и очки за рефералов
        new_ref_count = current_ref_count + 1
        new_ref_points = current_ref_points + REFERRAL_REWARD
        cursor.execute(
            "UPDATE users SET NUM_OF_REFS = ?, REF_POINTS = ? WHERE USER_ID = ?",
            (new_ref_count, new_ref_points, referrer_id)
        )
        conn.commit()
        print(f"Referral count for user {referrer_id} incremented to {new_ref_count}.")
        print(f"Referral points for user {referrer_id} incremented to {new_ref_points}.")
    except Exception as e:
        print(f"Error incrementing referral count or points for user {referrer_id}: {e}")
    finally:
        conn.close()


async def get_referrer(user_id: int) -> int | None:
    """
    Возвращает идентификатор реферера для указанного пользователя.

    Параметры:
    - user_id (int): Уникальный идентификатор пользователя.

    Возвращает:
    - referrer_id (int): Идентификатор пользователя-реферера, если он существует.
    - None, если реферер не найден или произошла ошибка.

    Примечание:
    Функция использует SQL-запрос для получения идентификатора реферера (REF_BY_USER)
    для указанного пользователя из таблицы `users`.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT REF_BY_USER FROM users WHERE USER_ID = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Error retrieving referrer for user {user_id}: {e}")
        return None

async def check_wallet_exists(wallet_address: str) -> bool:
    """
    Проверяет, отсутствует ли запись с указанным кошельком в базе данных.

    Параметры:
    - wallet_address (str): Адрес кошелька для проверки.

    Возвращает:
    - True, если запись с указанным кошельком отсутствует в базе данных.
    - False, если запись с указанным кошельком найдена в базе данных или произошла ошибка.

    Примечание:
    Функция использует SQL-запрос для проверки наличия записи с указанным кошельком в таблице `users`.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        # Выполняем SQL-запрос для проверки наличия кошелька
        cursor.execute("SELECT 1 FROM users WHERE ADDR = ?", (wallet_address,))
        result = cursor.fetchone()
        conn.close()

        # Проверяем, если результат пустой, значит запись не найдена
        return result is None
    except Exception as e:
        print(f"Error checking wallet address in database: {e}")
        return False