from aiogram import types, Router
from aiogram.filters import CommandStart
from messages.basic_messages import messages
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from FSM.states import CaptchaState, RegestrationState
from DB.database_logic import check_is_user_already_here, add_user_to_db, add_referrer_to_user
from keyboards.menu_kb import menu_kb_ru, menu_kb_eng
from logic.refs import get_refferer_id

standard_handler_router = Router()


def get_message(messages, message_key, language, **kwargs) -> str:
    """
    Retrieve a message based on the key and language,
    formatting it with any provided keyword arguments.
    examples:
        capture_message = get_message(messages, "WELCOME_MESSAGE", "ENG")
        print(capture_message)
        capture_message = get_message(messages, "WELCOME_MESSAGE", "RU", user_name='дурачок')
        print(capture_message)
    """
    print("def get_message")
    # Retrieve the default values and specific message template
    defaults = messages.get("default_values", {})
    message_template = messages.get(message_key, {}).get(language)

    # If the message template exists, use it; otherwise, return a fallback message
    if message_template:
        # Update the default values dictionary with any keyword arguments provided
        all_kwargs = {**defaults, **kwargs}
        return message_template.format(**all_kwargs)
    else:
        return "Message not available."


# Handler под команду /start
@standard_handler_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    print("Processing /start command...")
    if check_is_user_already_here(message.from_user.id):
        print("User already in db")
        await generate_captcha(message)
        await state.set_state(CaptchaState.wait_captcha_state)
        capture_message = get_message(messages, "CAPTCHA_MESSAGE", "ENG")
        await message.answer(text=capture_message)
        # Запуск меню после капчи
    else:
        print("User not in db")
        add_user_to_db(message.from_user.id)
        refferer = get_refferer_id(message.text)
        if refferer is not None:
            add_referrer_to_user(message.from_user.id, refferer)
        await generate_captcha(message)
        await state.set_state(RegestrationState.captcha_state)
        capture_message = get_message(messages, "CAPTCHA_MESSAGE", "ENG")
        await message.answer(text=capture_message)
