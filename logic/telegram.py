from settings.config import bot
from settings.config import TELEGRAM_LINKS


async def check_joined_telegram_channel(user_id):
    """
     Проверяет, является ли пользователь участником указанных Telegram-каналов.

     Параметры:
     - user_id (int): Уникальный идентификатор пользователя Telegram.

     Возвращает:
     - True, если пользователь является участником всех указанных каналов.
     - False, если пользователь не состоит хотя бы в одном из указанных каналов или возникла ошибка при проверке.

     Функция проходит по списку каналов, указанных в TELEGRAM_LINKS, проверяет статус пользователя
     в каждом канале и возвращает False, если пользователь не является членом одного или более каналов.
     Возможные статусы пользователя, указывающие на его отсутствие в канале:
     - 'left': пользователь покинул канал.
     - 'kicked': пользователь был исключен из канала.
     - 'banned': пользователь был заблокирован в канале.

     В случае возникновения ошибки при проверке членства, функция также возвращает False.

     Исключения:
     - Любые исключения, возникшие при проверке членства, перехватываются и выводятся в консоль.
     """
    try:
        links = TELEGRAM_LINKS.split("\n")
        for link in links:
            username = "@" + link.split("/")[-1]  # Получаем username канала из ссылки
            member = await bot.get_chat_member(chat_id=username, user_id=user_id)
            # Проверяем статус пользователя в канале
            if member.status in ('left', 'kicked', 'banned'):
                return False
    except Exception as e:
        print(f"Error checking channel membership: {e}")
        return False
    return True
