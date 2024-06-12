import re
import logging
from settings.logging_config import get_logger

logger = get_logger()


def is_valid_crypto_address(crypto_address: str) -> bool:
    """
    Проверяет, является ли криптоадрес допустимым.

    Параметры:
    - crypto_address (str): Криптоадрес для проверки.

    Возвращает:
    - True, если криптоадрес соответствует заданному формату.
    - False, если криптоадрес не соответствует формату.

    Примечание:
    Функция использует регулярное выражение для проверки, соответствует ли криптоадрес
    следующему формату: Опциональная буква 'U' или 'E' в начале, за которой следует 48
    символов, включающих буквы, цифры, дефисы и символы подчеркивания.
    """
    crypto_regex = re.compile(r'^[UE]?[0-9A-Za-z\-_]{48}$')
    match = crypto_regex.match(crypto_address)
    if match:
        logger.info(f"Crypto address {crypto_address} is valid.")
        return True
    else:
        logger.warning(f"Crypto address {crypto_address} is invalid.")
        return False
