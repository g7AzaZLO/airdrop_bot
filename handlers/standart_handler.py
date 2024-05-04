from aiogram import types, Router
from aiogram.filters import CommandStart
from messages.basic_messages import messages
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from FSM.states import CaptchaState

standart_handler_router = Router()


def get_message(messages, message_key, language, **kwargs):
    """
    Retrieve a message based on the key and language,
    formatting it with any provided keyword arguments.
    """
    message_template = messages.get(message_key, {}).get(language)
    if message_template:
        return message_template.format(**kwargs)
    else:
        # Return a default message if the specific language or key is not found
        return "Message not available."


# Handler под команду /start
@standart_handler_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    print("Processing /start command...")
    await generate_captcha(message)
    await state.set_state(CaptchaState.wait_captcha_state)
    capture_message = get_message(messages, "WELCOME_MESSAGE", "ENG")
    await message.answer(text=capture_message)


# Handler состояния капчи
@standart_handler_router.message(CaptchaState.wait_captcha_state)
async def captcha_response_handler(message: types.Message, state: FSMContext) -> None:
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    user_answer = await state.get_data()
    result = await check_captcha(message, user_answer)
    if result:
        await state.clear()
