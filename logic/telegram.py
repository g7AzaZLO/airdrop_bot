from settings.config import bot
from settings.config import TELEGRAM_LINKS


async def check_joined_channel(user_id):
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
