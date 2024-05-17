from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from messages.basic_messages import messages
from messages.other_messages import other_messages
from logic.captcha import generate_captcha
from aiogram.fsm.context import FSMContext
from FSM.states import CaptchaState, RegistrationState, AdminMessageState
from DB.database_logic import check_is_user_already_here, add_user_to_db, add_referrer_to_user, get_language_for_user
from logic.refs import get_refferer_id
from settings.config import ADMINS_IDS

standard_handler_router = Router()


async def get_message(messages: dict, message_key: str, language: str, **kwargs) -> str:
    """
    Retrieve a message based on the key and language,
    formatting it with any provided keyword arguments.
    examples:
        capture_message = get_message(messages, "WELCOME_MESSAGE", "ENG")
        print(capture_message)
        capture_message = get_message(messages, "WELCOME_MESSAGE", "RU", user_name='дурачок')
        print(capture_message)
    """
    # print("def get_message")
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
@standard_handler_router.message(CommandStart(), F.chat.type == "private")
async def start(message: types.Message, state: FSMContext) -> None:
    print("Processing /start command...")
    user_id = message.from_user.id
    if await check_is_user_already_here(user_id):
        print("User already in db")
        await generate_captcha(message)
        await state.set_state(CaptchaState.wait_captcha_state)
        capture_message = await get_message(messages, "CAPTCHA_MESSAGE", "ENG")
        await message.answer(text=capture_message, reply_markup=types.ReplyKeyboardRemove())
        # Запуск меню после капчи
    else:
        print("User not in db")
        await add_user_to_db(user_id)
        refferer = await get_refferer_id(message.text)
        if refferer is not None:
            await add_referrer_to_user(user_id, refferer)
        await generate_captcha(message)
        await state.set_state(RegistrationState.captcha_state)
        capture_message = await get_message(messages, "CAPTCHA_MESSAGE", "ENG")
        await message.answer(text=capture_message, reply_markup=types.ReplyKeyboardRemove())


@standard_handler_router.message(Command("message"), F.chat.type == "private")
async def start_message_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    language = await get_language_for_user(user_id)
    if message.from_user.id not in ADMINS_IDS:
        await message.answer("У вас нет прав для выполнения этого действия.")
        return
    reply = await get_message(other_messages,"ENTER_MESSAGE_TEXT", language)
    await message.answer(text=reply)
    await state.set_state(AdminMessageState.waiting_for_message)
