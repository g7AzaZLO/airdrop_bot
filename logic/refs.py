import logging
from settings.config import BOT_NICKNAME
from settings.logging_config import get_logger

logger = get_logger()


async def get_refferal_link(user_id: int) -> str:
    """
    Функция возвращает ссылку для реферальной программы.
    """
    referral_link = f"https://t.me/{BOT_NICKNAME}?start={user_id}"
    logger.info(f"Generated referral link for user {user_id}: {referral_link}")
    return referral_link


async def get_refferer_id(link: str) -> int | None:
    """"
    Функция возвращает id реферера из ссылки.
    """
    logger.info("get_refferer_id")
    try:
        referrer_id = int(link[7:])
        logger.info(f"Extracted referrer id: {referrer_id}")
        return referrer_id
    except ValueError as e:
        logger.error(f"Error extracting referrer id from link '{link}': {e}")
        return None
