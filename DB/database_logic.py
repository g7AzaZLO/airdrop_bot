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
    - NUM_OF_REFS (INT) - количетсов рефералов
    - REF_BY_USER (INTEGER) - user_id ользователя чьим рефералом является
    - TWITTER_USER (TEXT) - ссылка на твиттер пользователя

    Печатает соответствующее сообщение о наличии или создании базы данных.
    """
    if isfile(DATABASE_FILE):
        print("Database exists...")
    else:
        print("Creating Database...")
        execute_non_query("CREATE TABLE users (USER_ID INTEGER, ADDR TEXT, ALREADY_REG BOOL, NUM_OF_REFS INT, REF_BY_USER INTEGER, TWITTER_USER TEXT);")
        print("Database created successfully")


def execute_non_query(command) -> None:
    """
    Выполняет SQL-команду, не возвращающую данные (например, INSERT, UPDATE, DELETE, CREATE).

    Параметры:
    - command (str): SQL-команда для выполнения.

    Открывает соединение с базой данных, указанной в переменной DATABASE_FILE, выполняет команду,
    фиксирует изменения и закрывает соединение. Это обеспечивает безопасное выполнение команд,
    изменяющих данные или структуру базы данных.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute(command)
    conn.commit()
    conn.close()
