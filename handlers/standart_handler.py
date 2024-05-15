from aiogram import types, Router
from aiogram.filters import CommandStart
from messages.basic_messages import messages
from aiogram.filters import Command
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from FSM.states import CaptchaState, RegistrationState
from DB.database_logic import check_is_user_already_here, add_user_to_db, add_referrer_to_user
from keyboards.menu_kb import menu_kb
from logic.refs import get_refferer_id
from DB.database_logic import get_language_for_user
from messages.menu_messages import menu_messages
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
@standard_handler_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    print("Processing /start command...")
    user_id = message.from_user.id
    if await check_is_user_already_here(user_id):
        print("User already in db")
        await generate_captcha(message)
        await state.set_state(CaptchaState.wait_captcha_state)
        capture_message = await get_message(messages, "CAPTCHA_MESSAGE", "ENG")
        await message.answer(text=capture_message)
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
        await message.answer(text=capture_message)


# @standard_handler_router.message(Command('menu'), Command('Menu'))
# async def menu(message: types.Message, state: FSMContext) -> None:
#     print("Processing /menu command...")
#     language = await get_language_for_user(message.from_user.id)
#     if await check_is_user_already_here(message.from_user.id):
#         print("User already in db")
#         await state.set_state(RegistrationState.main_menu_state)
#         reply = await get_message(menu_messages, "MENU", language)
#         await message.answer(text=reply, reply_markup=menu_kb[language])
#         # Запуск меню после капчи
#     else:
#         print("User not in db")
#         await add_user_to_db(message.from_user.id)
#         refferer = await get_refferer_id(message.text)
#         if refferer is not None:
#             await add_referrer_to_user(message.from_user.id, refferer)
#         await generate_captcha(message)
#         await state.set_state(RegistrationState.captcha_state)
#         capture_message = await get_message(messages, "CAPTCHA_MESSAGE", "ENG")
#         await message.answer(text=capture_message)
