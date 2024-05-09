import sqlite3
import re
from settings.config import DATABASE_FILE


async def check_joined_twitter_channel(user_twitter_link: str) -> bool:
    """
    Проверяет, существует ли запись с указанной ссылкой на Twitter в базе данных.

    Параметры:
    - user_twitter_link (str): Ссылка на профиль пользователя в Twitter.

    Возвращает:
    - True, если ссылка существует в базе данных.
    - False, если ссылка не найдена в базе данных или произошла ошибка.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        # Выполняем SQL-запрос для проверки наличия ссылки
        cursor.execute("SELECT 1 FROM users WHERE TWITTER_USER = ?", (user_twitter_link,))
        result = cursor.fetchone()
        conn.close()

        # Проверяем, если результат не пустой, значит запись найдена
        return result is None
    except Exception as e:
        print(f"Error checking Twitter link in database: {e}")
        return False


def is_valid_twitter_link(twitter_link: str) -> bool:
    """
    Проверяет, является ли ссылка допустимой ссылкой на профиль Twitter.

    Параметры:
    - twitter_link (str): Ссылка на профиль пользователя в Twitter.

    Возвращает:
    - True, если ссылка является допустимой ссылкой на профиль Twitter.
    - False, если ссылка не соответствует ожидаемому формату.

    Примечание:
    Функция использует регулярное выражение для проверки, соответствует ли ссылка формату
    `https://twitter.com/username`, где `username` может содержать от 1 до 20 символов,
    включающих буквы, цифры и символы подчеркивания.
    """
    twitter_regex = re.compile(
        r'^(https?://)?(www\.)?twitter\.com/([A-Za-z0-9_]{1,20})/?$'
    )
    match = twitter_regex.match(twitter_link)
    return match is not None
