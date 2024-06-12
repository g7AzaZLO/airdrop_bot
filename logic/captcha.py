import os
from multicolorcaptcha import CaptchaGenerator
from aiogram import types
from settings.logging_config import get_logger

logger = get_logger()
captcha_data = {}


async def check_captcha(message: types.Message) -> bool:
    """
    Проверяет правильность ответа пользователя на капчу.

    Параметры:
    - message: сообщение пользователя с ответом на капчу.
    - captcha_data: словарь, содержащий данные капчи для каждого пользователя.

    Возвращает:
    - True, если ответ пользователя правильный, иначе False.
    """
    logger.info("def check_captcha")
    try:
        user_id = message.from_user.id
        if user_id not in captcha_data:
            await generate_captcha(message)
            return False

        captcha_text = captcha_data[user_id]
        user_input = message.text

        if captcha_text != user_input:
            await message.reply("Incorrect CAPTCHA, please try again.")
            logger.warning(f"User {user_id} entered incorrect CAPTCHA: {user_input}")
            await generate_captcha(message)
            return False
        else:
            await message.reply("Correct CAPTCHA!")
            logger.info(f"User {user_id} entered correct CAPTCHA.")
            return True
    except Exception as e:
        user_id = message.from_user.id
        logger.error(f"Error while checking CAPTCHA for user {user_id}: {e}")
        return False


async def generate_captcha(message: types.Message) -> None:
    """
    Генерирует капчу и отправляет её пользователю.

    Параметры:
    - message: сообщение для отправки капчи.
    """
    logger.info("def generate_captcha")
    try:
        captcha_generator = CaptchaGenerator()
        captcha = captcha_generator.gen_captcha_image()
        captcha_data[message.from_user.id] = captcha.characters
        filename = f"{message.from_user.id}.png"
        captcha.image.save(filename, "PNG")
        await message.reply_photo(photo=types.FSInputFile(path=filename))
        logger.info(f"CAPTCHA generated and sent to user {message.from_user.id}")
        os.remove(filename)
    except Exception as e:
        logger.error(f"Error generating CAPTCHA for user {message.from_user.id}: {e}")