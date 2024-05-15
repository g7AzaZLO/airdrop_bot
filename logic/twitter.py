import re
from DB.mongo import users_collection


async def check_joined_twitter_channel(user_twitter_link: str) -> bool:
    """
    Проверяет, существует ли запись с указанной ссылкой на Twitter в базе данных MongoDB.

    Параметры:
    - user_twitter_link (str): Ссылка на профиль пользователя в Twitter.

    Возвращает:
    - True, если ссылка не существует в базе данных.
    - False, если ссылка найдена в базе данных или произошла ошибка.
    """
    print("def check_joined_twitter_channel")
    try:
        result = await users_collection.find_one({"TWITTER_USER": user_twitter_link})
        if result:
            print(f"Twitter link {user_twitter_link} found in database.")
            return False
        else:
            print(f"Twitter link {user_twitter_link} not found in database.")
            return True
    except Exception as e:
        print(f"Error checking Twitter link in MongoDB: {e}")
        return True


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
