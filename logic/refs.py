from settings.config import BOT_NICKNAME


async def get_refferal_link(user_id: int) -> str:
    """
    Функция возвращает ссылку для реферальной программы.
    """
    print(f"https://t.me/{BOT_NICKNAME}?start={user_id}")
    return f"https://t.me/{BOT_NICKNAME}?start={user_id}"


async def get_refferer_id(link: str) -> str:
    """"
    Функция возвращает id реферера из ссылки.
    """
    print(link[7:])
    return link[7:]
