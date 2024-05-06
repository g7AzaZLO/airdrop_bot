import sqlite3
from settings.config import DATABASE_FILE
from os.path import isfile


def initialize_db() -> None:
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

    Печатает соответствующее сообщение о наличии или создании базы данных.
    """
    if isfile(DATABASE_FILE):
        print("Database exists...")
    else:
        print("Creating Database...")
        execute_non_query(
            "CREATE TABLE users (USER_ID INTEGER, ADDR TEXT, ALREADY_REG BOOL, NUM_OF_REFS INT, REF_BY_USER INTEGER, TWITTER_USER TEXT, LANGUAGE TEXT);")
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


def delete_user_from_db(user_id: int) -> bool:
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


def check_is_user_already_here(user_id: int) -> bool:
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

def register_user(user_id: int, addr: str, twitter_user: str, language: str):
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
        cursor.execute("INSERT INTO users (USER_ID, ADDR, ALREADY_REG, NUM_OF_REFS, TWITTER_USER, LANGUAGE) VALUES (?, ?, ?, ?, ?, ?)", (user_id, addr, True, 0, twitter_user, language))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def update_user_details(user_id: int, **kwargs) -> bool:
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
    
    
def get_user_details(user_id: int):
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
    
def list_users_by_filter(**filters):
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

def update_language_in_db(user_id: int, language: str) -> None:
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

def add_user_to_db(user_id):
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
        

def get_language_for_user(user_id: int) -> str:
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
