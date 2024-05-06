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


def check_is_user_already_here(user_id: int) ->bool:
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
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE USER_ID = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return len(rows) == 0
    except Exception as e:
        print(e)
        return False
