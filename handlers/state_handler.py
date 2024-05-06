from aiogram import types, Router
from FSM.states import CaptchaState, RegestrationState
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from handlers.standart_handler import get_message
from messages.basic_messages import messages
from keyboards.small_kb import join_kb_eng, join_kb_ru, language_choose_kb
from DB.database_logic import update_language_in_db

state_handler_router = Router()


# Handler состояния капчи в CaptchaState
@state_handler_router.message(CaptchaState.wait_captcha_state)
async def captcha_response_handler(message: types.Message, state: FSMContext) -> None:
    print("def captcha_response_handler")
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    result = await check_captcha(message)
    if result:
        await state.clear()
        # await state.main_menu


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
    language = None

    if user_response == "ENG English":
        language = "ENG"
        await state.set_state(RegestrationState.hello_state)
        await message.answer(text=(get_message(messages, "WELCOME_MESSAGE", "ENG")), reply_markup=join_kb_eng)
    elif user_response == "RU Русский":
        language = "RU"
        await state.set_state(RegestrationState.hello_state)
        await message.answer(text=(get_message(messages, "WELCOME_MESSAGE", "RU")), reply_markup=join_kb_ru)
    else:
        await message.answer(text="That language is not on the list")
        await state.set_state(RegestrationState.lang_choose_state)
        return

    # Вызываем функцию для обновления языка пользователя в базе данных
    update_language_in_db(user_id, language)


@state_handler_router.message(RegestrationState.hello_state)
async def hello_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def hello_response_handler")
    user_response = message.text
    await state.update_data(user_hello_response=user_response)
    if user_response == "🚀 Join Airdrop" or "🚀 Присоединиться к аирдропу":
        await state.set_state(RegestrationState.hello_state)
