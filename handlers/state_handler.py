from aiogram import types, Router
from FSM.states import CaptchaState, RegestrationState
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from handlers.standart_handler import get_message
from messages.basic_messages import messages
from keyboards.small_kb import join_kb, language_choose_kb, yes_no_kb, sub_cancel_kb, social_join_kb, kb_start
from DB.database_logic import update_language_in_db, get_language_for_user, delete_user_from_db
from keyboards.menu_kb import menu_kb
from logic.telegram import check_joined_telegram_channel
from DB.database_logic import check_is_user_already_here, add_user_to_db, add_referrer_to_user, get_referrer, increment_referrer_count
from logic.refs import get_refferer_id, get_refferal_link
from logic.twitter import check_joined_twitter_channel, is_valid_twitter_link
from logic.address import is_valid_crypto_address

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
            reply = get_message(messages, "LANGUAGE_CHOOSE", "ENG")
            await message.answer(text=reply, reply_markup=language_choose_kb)


# Handler состояния капчи в регистрации пользователя
@state_handler_router.message(RegestrationState.captcha_state)
async def captcha_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def captcha_response_handler_in_reg")
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    result = await check_captcha(message)
    if result:
        await state.set_state(RegestrationState.lang_choose_state)
        reply = get_message(messages, "LANGUAGE_CHOOSE", "ENG")
        await message.answer(text=reply, reply_markup=language_choose_kb)


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
        reply = get_message(messages, "LANGUAGE_CHOSEN_WRONG", "ENG")
        await message.answer(text=reply, reply_markup=language_choose_kb)
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
        await state.update_data(
            state_end1=CaptchaState.null_state,
            state_end2=RegestrationState.hello_state,
            text1=get_message(messages, "START_AGAIN_TEXT", language),
            text2=get_message(messages, "WELCOME_MESSAGE", language, user_name=message.from_user.first_name),
            kb1=kb_start,
            kb2=join_kb[language],
            delete=True
        )
        reply = get_message(messages, "YES_NO", language)
        await message.answer(text=reply, reply_markup=yes_no_kb[language])
        await state.set_state(RegestrationState.yes_no_state)
    else:
        await message.answer(
            text=(get_message(messages, "WELCOME_MESSAGE", language, user_name=message.from_user.first_name)),
            reply_markup=join_kb[language],
            parse_mode="MARKDOWN")
        return


@state_handler_router.message(RegestrationState.proceed_state)
async def proceed_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def proceed_response_handler_in_reg")
    user_response = message.text
    language = get_language_for_user(message.from_user.id)
    await state.update_data(user_proceed_response=user_response)
    if user_response in ["✅ Согласен с правилами", "✅ Submit Details"]:
        await state.set_state(RegestrationState.follow_telegram_state)
        reply = get_message(messages, "MAKE_SURE_TELEGRAM", language)
        await message.answer(text=reply, reply_markup=social_join_kb[language])
    elif user_response in ["❌ Cancel", "❌ Отказаться"]:
        await state.update_data(
            state_end1=CaptchaState.null_state,
            state_end2=RegestrationState.proceed_state,
            text1=get_message(messages, "START_AGAIN_TEXT", language),
            text2=get_message(messages, "PROCEED_MESSAGE", language),
            kb1=kb_start,
            kb2=sub_cancel_kb[language],
            delete=True
        )
        reply = get_message(messages, "YES_NO", language)
        await message.answer(text=reply, reply_markup=yes_no_kb[language])
        await state.set_state(RegestrationState.yes_no_state)
    else:
        reply = get_message(messages, "PROCEED_MESSAGE", language)
        await message.answer(text=reply, reply_markup=sub_cancel_kb[language], parse_mode="MARKDOWN")
        return


@state_handler_router.message(RegestrationState.follow_telegram_state)
async def follow_telegram_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def follow_telegram_response_handler")
    user_response = message.text
    language = get_language_for_user(message.from_user.id)
    await state.update_data(user_follow_telegram_response=user_response)
    if user_response in ["✅ Вступил", "✅ Joined"]:
        if await check_joined_telegram_channel(message.from_user.id):
            print("Yes, user in all telegram channel")
            await state.set_state(RegestrationState.follow_twitter_state)
            reply1 = get_message(messages, "FOLLOW_TWITTER_TEXT", language)
            reply2 = get_message(messages, "GET_TWITTER_LINK_TEXT", language)
            await message.answer(text=reply1, reply_markup=types.ReplyKeyboardRemove())
            await message.answer(text=reply2)
        else:
            print("NO HE ISNT HERE")
            await state.set_state(RegestrationState.follow_telegram_state)
            reply = get_message(messages, "NOT_SUB_AT_GROUP_TEXT", language)
            await message.answer(text=reply, reply_markup=social_join_kb[language])
    else:
        reply = get_message(messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply)
        await state.set_state(RegestrationState.follow_telegram_state)


@state_handler_router.message(RegestrationState.follow_twitter_state)
async def follow_twitter_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def follow_twitter_response_handler")
    user_response = message.text
    language = get_language_for_user(message.from_user.id)
    await state.update_data(user_follow_twitter_response=user_response)
    if is_valid_twitter_link(user_response):
        if await check_joined_twitter_channel(user_response):
            print("all ok")
            await state.set_state(RegestrationState.submit_address_state)
            reply = get_message(messages, "SUBMIT_ADDRESS_TEXT", language)
            await message.answer(text=reply, reply_markup=types.ReplyKeyboardRemove(), parse_mode="MARKDOWN")
        else:
            print("already in base")
            await state.set_state(RegestrationState.follow_twitter_state)
            reply = get_message(messages, "TWITTER_ALREADY_REGISTERED_TEXT", language)
            await message.answer(text=reply)
    else:
        print("Invalid Twitter Link")
        await state.set_state(RegestrationState.follow_twitter_state)
        reply = get_message(messages, "TWITTER_INVALID_LINK_TEXT", language)
        await message.answer(text=reply)


@state_handler_router.message(RegestrationState.submit_address_state)
async def submit_address_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def submit_address_response_handler_in_reg")
    user_response = message.text
    language = get_language_for_user(message.from_user.id)
    await state.update_data(user_submit_address_response=user_response)
    if is_valid_crypto_address(user_response):
        print("Valid crypto address")
        await state.set_state(RegestrationState.main_menu_state)
        ref_link = await get_refferal_link(message.from_user.id)
        reply = get_message(messages, "JOINED_TEXT", language, referral_link=ref_link)
        await message.answer(text=reply, reply_markup=menu_kb[language], parse_mode="MARKDOWN")
        refferer = get_referrer(message.from_user.id)
        if refferer is not None:
            increment_referrer_count(refferer)
    else:
        print("Invalid crypto address")
        await state.set_state(RegestrationState.submit_address_state)
        reply = get_message(messages, "INVALID_ADDRESS_TEXT", language)
        await message.answer(text=reply)


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
        reply = get_message(messages, "UKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply)
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
        reply = get_message(messages, "LANGUAGE_CHOSEN_WRONG", "ENG")
        await message.answer(text=reply, reply_markup=language_choose_kb)
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
    delete = data.get('delete')
    user_response = message.text
    await state.update_data(user_hello_response=user_response)
    language = get_language_for_user(message.from_user.id)
    if user_response in ["Да", "Yes"]:
        if delete:
            delete_user_from_db(message.from_user.id)
        await state.set_state(state_end1)
        if text1 is not None and kb1 is None:
            await message.answer(text=text1, reply_markup=types.ReplyKeyboardRemove(), parse_mode="MARKDOWN")
        elif text1 is not None and kb1 is not None:
            await message.answer(text=text1, reply_markup=kb1, parse_mode="MARKDOWN")
    elif user_response in ["Нет", "No"]:
        await state.set_state(state_end2)
        if text2 is not None and kb2 is None:
            await message.answer(text=text2, reply_markup=types.ReplyKeyboardRemove(), parse_mode="MARKDOWN")
        elif text2 is not None and kb2 is not None:
            await message.answer(text=text2, reply_markup=kb2, parse_mode="MARKDOWN")
    else:
        reply = get_message(messages, "YES_NO", language)
        await message.answer(text=reply, reply_markup=yes_no_kb[language])


@state_handler_router.message(CaptchaState.null_state)
async def null_state(message: types.Message, state: FSMContext) -> None:
    print("def null_state")
    user_response = message.text
    language = get_language_for_user(message.from_user.id)
    if language is None: language = "ENG"
    if user_response in ["start", "Start", "Начать", "начать",
                         r"\Начать", r"\начать", r"\start", r"\Start", ]:
        if check_is_user_already_here(message.from_user.id):
            print("User already in db")
            await generate_captcha(message)
            await state.set_state(CaptchaState.wait_captcha_state)
            capture_message = get_message(messages, "CAPTCHA_MESSAGE", language)
            await message.answer(text=capture_message, reply_markup=types.ReplyKeyboardRemove())
        # Запуск меню после капчи
        else:
            print("User not in db")
            add_user_to_db(message.from_user.id)
            refferer = await get_refferer_id(message.text)
            if refferer is not None:
                add_referrer_to_user(message.from_user.id, refferer)
            await generate_captcha(message)
            await state.set_state(RegestrationState.captcha_state)
            capture_message = get_message(messages, "CAPTCHA_MESSAGE", language)
            await message.answer(text=capture_message, reply_markup=types.ReplyKeyboardRemove())
    else:
        reply = get_message(messages, "START_AGAIN_TEXT", language)
        await message.answer(text=reply, reply_markup=kb_start)
        return
    

