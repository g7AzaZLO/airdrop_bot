from aiogram import types, Router
from FSM.states import CaptchaState, RegestrationState
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from handlers.standart_handler import get_message
from messages.basic_messages import messages
from keyboards.small_kb import join_kb_eng, join_kb_ru, language_choose_kb
from DB.database_logic import update_language_in_db, get_language_for_user
from keyboards.menu_kb import menu_kb
from aiogram.filters import Command

state_handler_router = Router()


# Handler состояния капчи в CaptchaState
@state_handler_router.message(CaptchaState.wait_captcha_state)
async def captcha_response_handler(message: types.Message, state: FSMContext) -> None:
    print("def captcha_response_handler")
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    result = await check_captcha(message)
    if result:
        # await state.clear()
        await state.set_state(RegestrationState.main_menu_state)
        language = get_language_for_user(message.from_user.id)
        reply = get_message(messages, "LANGUAGE_CHOSEN", language)
        await message.answer(text=reply, reply_markup=menu_kb[language])
        if language not in ["ENG", "RU"]:
            await state.set_state(RegestrationState.lang_choose_state)
            await message.answer(text="Please choose your language", reply_markup=language_choose_kb)


# Handler состояния капчи в регистрации пользователя
@state_handler_router.message(RegestrationState.captcha_state)
async def captcha_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def captcha_response_handler_in_reg")
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    result = await check_captcha(message)
    if result:
        await state.set_state(RegestrationState.lang_choose_state)
        await message.answer(text="Please choose your language", reply_markup=language_choose_kb)


@state_handler_router.message(RegestrationState.lang_choose_state)
async def lang_choose_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def lang_choose_response_handler_in_reg")
    user_response = message.text
    await state.update_data(user_lang_choose_response=user_response)

    user_id = message.from_user.id  # Идентификатор пользователя для SQL запроса
    if user_response == "ENG English":
        language = "ENG"
        await state.set_state(RegestrationState.hello_state)
        await message.answer(
            text=(get_message(messages, "WELCOME_MESSAGE", "ENG", user_name=message.from_user.first_name)),
            reply_markup=join_kb_eng,
            parse_mode="MARKDOWN")
    elif user_response == "RU Русский":
        language = "RU"
        await state.set_state(RegestrationState.hello_state)
        await message.answer(
            text=(get_message(messages, "WELCOME_MESSAGE", "RU", user_name=message.from_user.first_name)),
            reply_markup=join_kb_ru,
            parse_mode="MARKDOWN")
    else:
        await message.answer(text="That language is not on the list")
        await message.answer(text="Please choose your language", reply_markup=language_choose_kb)
        await state.set_state(RegestrationState.lang_choose_state_again)
        return
    # Вызываем функцию для обновления языка пользователя в базе данных
    update_language_in_db(user_id, language)


@state_handler_router.message(RegestrationState.lang_choose_state_again)
async def lang_choose_response_handler(message: types.Message, state: FSMContext) -> None:
    print("def lang_choose_response_handler")
    user_response = message.text
    await state.update_data(user_lang_choose_response=user_response)

    user_id = message.from_user.id  # Идентификатор пользователя для SQL запроса
    if user_response == "ENG English":
        language = "ENG"
        await state.set_state(RegestrationState.main_menu_state)
        reply = get_message(messages, "LANGUAGE_CHOSEN", language)
        await message.answer(text=reply, reply_markup=menu_kb[language])
    elif user_response == "RU Русский":
        language = "RU"
        await state.set_state(RegestrationState.main_menu_state)
        reply = get_message(messages, "LANGUAGE_CHOSEN", language)
        await message.answer(text=reply, reply_markup=menu_kb[language])
    else:
        await message.answer(text="That language is not on the list")
        await message.answer(text="Please choose your language", reply_markup=language_choose_kb)
        return
    # Вызываем функцию для обновления языка пользователя в базе данных
    update_language_in_db(user_id, language)


@state_handler_router.message(RegestrationState.hello_state)
async def hello_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def hello_response_handler")
    user_response = message.text
    await state.update_data(user_hello_response=user_response)
    if user_response in ["🚀 Join Airdrop", "🚀 Присоединиться к аирдропу"]:
        await state.set_state(RegestrationState.main_menu_state)
        language = get_language_for_user(message.from_user.id)
        # get_message(messages, "WELCOME_MESSAGE", "ENG")
        reply = get_message(messages, "LANGUAGE_CHOSEN", language)
        await message.answer(text=reply, reply_markup=menu_kb[language])
    elif user_response in ["❌ Cancel", "❌ Отказаться"]:
        # ADD STUFF HERE (WHAT ARE WE DOING IF THEY CHOOSE CANCEL)
        print("CANCELLED and we don't have the handler")
        return


@state_handler_router.message(RegestrationState.main_menu_state)
async def main_menu_handler(message: types.Message, state: FSMContext) -> None:
    user_response = message.text
    print(f"def main_menu_handler, user response {user_response}")
    language = get_language_for_user(message.from_user.id)
    if user_response in ["Profile", "Профиль"]:
        reply = get_message(messages, "PROFILE_MENU", language, user_name=message.from_user.first_name)
        await message.answer(text=reply, reply_markup=menu_kb[language])
        print(f"deleted {language}")
        return
    elif user_response in ["Change Language", "Сменить Язык"]:
        reply = get_message(messages, "LANGUAGE_CHOOSE", language)
        await message.answer(text=reply, reply_markup=language_choose_kb)
        await state.set_state(RegestrationState.lang_choose_state_again)
    else:
        # Handle other cases or unknown commands
        await message.answer("Unknown command, please choose from the menu.")
        # Ensure we go back to the main menu state
        await state.set_state(RegestrationState.main_menu_state)
