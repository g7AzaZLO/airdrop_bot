from multicolorcaptcha import CaptchaGenerator
from aiogram import types


async def check_captcha(message: types.Message, captcha_data: dict) -> bool:
    """
    Проверяет правильность ответа пользователя на капчу.

    Параметры:
    - message: сообщение пользователя с ответом на капчу.
    - captcha_data: словарь, содержащий данные капчи для каждого пользователя.

    Возвращает:
    - True, если ответ пользователя правильный, иначе False.
    """
    try:
        user_id = message.from_user.id
        if user_id not in captcha_data:
            return False

        captcha_text = captcha_data[user_id]
        user_input = message.text

        if captcha_text != user_input:
            await message.reply("Неверная капча!")
            return False
        else:
            await message.reply("Правильно!")
            return True
    except Exception as e:
        print("Ошибка при проверке капчи:", e)
        return False
