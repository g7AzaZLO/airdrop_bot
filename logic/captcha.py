import os

from multicolorcaptcha import CaptchaGenerator
from aiogram import types

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
    print("def check_captcha")
    try:
        user_id = message.from_user.id
        if user_id not in captcha_data:
            # Generate a CAPTCHA if it's not already there, perhaps in case of error or restart
            await generate_captcha(message)
            return False

        captcha_text = captcha_data[user_id]
        user_input = message.text

        if captcha_text != user_input:
            await message.reply("Incorrect CAPTCHA, please try again.")
            await generate_captcha(message)
            return False
        else:
            await message.reply("Correct CAPTCHA!")
            return True
    except Exception as e:
        print("Error while checking CAPTCHA:", e)
        return False


async def generate_captcha(message: types.Message) -> None:
    """
    Генерирует капчу и отправляет её пользователю.

    Параметры:
    - message: сообщение для отправки капчи.
    """
    print("def generate_captcha")
    try:
        captcha_generator = CaptchaGenerator()
        captcha = captcha_generator.gen_captcha_image()

        # Сохраняем сгенерированный текст капчи для пользователя
        captcha_data[message.from_user.id] = captcha.characters

        # Сохраняем картинку для отправки
        filename = f"{message.from_user.id}.png"
        captcha.image.save(filename, "PNG")

        # Отправляем изображение капчи пользователю
        await message.reply_photo(photo=types.FSInputFile(path=filename))

        # Удаляем файл после отправки
        os.remove(filename)


    except Exception as e:
        print("Ошибка при генерации капчи:", e)
        if os.path.exists(filename):
            os.remove(filename)
