from aiogram import types, Router
from FSM.states import CaptchaState, RegestrationState
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from handlers.standart_handler import get_message
from messages.basic_messages import messages
from keyboards.small_kb import join_kb, language_choose_kb, yes_no_kb, sub_cancel_kb,telegram_join_kb
from DB.database_logic import update_language_in_db, get_language_for_user, delete_user_from_db
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
        reply = get_message(messages, "MENU", language)
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
    elif user_response == "RU Русский":
        language = "RU"
    else:
        await message.answer(text="That language is not on the list")
        await message.answer(text="Please choose your language", reply_markup=language_choose_kb)
        await state.set_state(RegestrationState.lang_choose_state_again)
        return
    await state.set_state(RegestrationState.hello_state)
    await message.answer(
        text=(get_message(messages, "WELCOME_MESSAGE", language, user_name=message.from_user.first_name)),
        reply_markup=join_kb[language],
        parse_mode="MARKDOWN")
    # Вызываем функцию для обновления языка пользователя в базе данных
    update_language_in_db(user_id, language)


@state_handler_router.message(RegestrationState.hello_state)
async def hello_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def hello_response_handler")
    user_response = message.text
    language = get_language_for_user(message.from_user.id)
    await state.update_data(user_hello_response=user_response)
    if user_response in ["🚀 Join Airdrop", "🚀 Присоединиться к аирдропу"]:
        await state.set_state(RegestrationState.proceed_state)
        reply = get_message(messages, "PROCEED_MESSAGE", language)
        await message.answer(text=reply, reply_markup=sub_cancel_kb[language], parse_mode="MARKDOWN")
    elif user_response in ["❌ Cancel", "❌ Отказаться"]:
        # ADD добавить состояние когда все отменено и все закрыто
        await state.update_data(
            state_end1=RegestrationState.hello_state,
            state_end2=RegestrationState.hello_state,
            text1=get_message(messages, "WELCOME_MESSAGE", language, user_name=message.from_user.first_name),
            text2=get_message(messages, "CANCEL_JOINING", language),
            kb1=join_kb[language],
            kb2=None
        )
        reply = get_message(messages, "YES_NO", language)
        await message.answer(text=reply, reply_markup=yes_no_kb[language])
        await state.set_state(RegestrationState.yes_no_state)
    else:
        pass

@state_handler_router.message(RegestrationState.proceed_state)
async def proceed_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def proceed_response_handler_in_reg")
    user_response = message.text
    language = get_language_for_user(message.from_user.id)
    await state.update_data(user_proceed_response=user_response)
    if user_response in ["✅ Согласен с правилами", "✅ Submit Details"]:
        await state.set_state(RegestrationState.follow_telegram_state)
        reply = get_message(messages, "MAKE_SURE_TELEGRAM", language)
        await message.answer(text=reply, reply_markup=telegram_join_kb[language])
    elif user_response in ["❌ Cancel", "❌ Отказаться"]:
        pass
    else:
        pass

@state_handler_router.message(RegestrationState.follow_telegram_state)
async def follow_telegram_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    pass

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


@state_handler_router.message(RegestrationState.lang_choose_state_again)
async def lang_choose_response_handler(message: types.Message, state: FSMContext) -> None:
    print("def lang_choose_response_handler")
    user_response = message.text
    await state.update_data(user_lang_choose_response=user_response)
    user_id = message.from_user.id  # Идентификатор пользователя для SQL запроса
    if user_response == "ENG English":
        language = "ENG"
    elif user_response == "RU Русский":
        language = "RU"
    else:
        await message.answer(text="That language is not on the list")
        await message.answer(text="Please choose your language", reply_markup=language_choose_kb)
        return
    await state.set_state(RegestrationState.main_menu_state)
    reply = get_message(messages, "MENU", language)
    await message.answer(text=reply, reply_markup=menu_kb[language])
    # Вызываем функцию для обновления языка пользователя в базе данных
    update_language_in_db(user_id, language)


@state_handler_router.message(RegestrationState.yes_no_state)
async def yes_no_reply(message: types.Message, state: FSMContext) -> None:
    print("def yes_no_reply")
    data = await state.get_data()
    state_end1 = data.get('state_end1')
    state_end2 = data.get('state_end2')
    text1 = data.get('text1')
    text2 = data.get('text2')
    kb1 = data.get('kb1')
    kb2 = data.get('kb2')
    user_response = message.text
    await state.update_data(user_hello_response=user_response)
    language = get_language_for_user(message.from_user.id)
    if user_response in ["ДА", "YES"]:
        await state.set_state(state_end1)
        if text1 is not None and kb1 is None:
            await message.answer(text=text1)
        elif text1 is not None and kb1 is not None:
            await message.answer(text=text1, reply_markup=kb1)
    elif user_response in ["НЕТ", "NO"]:
        await state.set_state(state_end2)
        if text2 is not None and kb2 is None:
            await message.answer(text=text2)
        elif text2 is not None and kb2 is not None:
            await message.answer(text=text2, reply_markup=kb2)
