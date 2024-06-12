import asyncio
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from messages.basic_messages import messages
from messages.menu_messages import menu_messages
from messages.task_menu_messages import task_menu_messages
from messages.other_messages import other_messages
from FSM.states import CaptchaState, RegistrationState, TasksState, state_messages, state_keyboards, \
    get_clean_state_identifier, state_menus, AdminMessageState
from keyboards.menu_kb import menu_kb, kb_menu_settings, create_numeric_keyboard
from keyboards.small_kb import join_kb, language_choose_kb, yes_no_kb, sub_cancel_kb, social_join_kb, kb_start, \
    kb_task_done_back, kb_tasks_back
from logic.refs import get_refferer_id, get_refferal_link
from logic.twitter import check_joined_twitter_channel, is_valid_twitter_link
from logic.address import is_valid_crypto_address
from logic.task import get_all_points, get_num_of_tasks, get_index_by_text_task, get_protection_from_task, \
    calculate_total_points, get_points_from_task, send_task_info, send_all_tasks_info, get_puzzle_from_task
from logic.captcha import generate_captcha, check_captcha
from logic.admins import ADMINS_IDS
from logic.telegram import check_joined_telegram_channel
from DB.database_logic import update_language_in_db, get_language_for_user, delete_user_from_db, get_user_details, \
    update_user_details, check_wallet_exists, decrement_referrer_count, mark_task_as_done, get_state_for_user, \
    set_user_state, remove_task_from_await, mark_task_as_await, delete_admin_message, insert_admin_messages, \
    get_admin_messages_dict, get_all_users
from DB.database_logic import check_is_user_already_here, add_user_to_db, add_referrer_to_user, get_referrer, \
    increment_referrer_count, add_points_to_user
from settings.config import AIRDROP_AMOUNT
from handlers.standart_handler import get_message
from settings.logging_config import get_logger

logger = get_logger()
state_handler_router = Router()


@state_handler_router.message(CaptchaState.wait_captcha_state)
async def captcha_response_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает ответ пользователя на капчу.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает ответ пользователя на капчу.
    - Проверяет правильность ответа.
    - Если ответ правильный, восстанавливает предыдущее состояние пользователя и отправляет соответствующее сообщение.
    """
    logger.debug("Executing captcha_response_handler")
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    result = await check_captcha(message)
    if result:
        user_id = message.from_user.id
        language = await get_language_for_user(message.from_user.id)
        current_state = await get_state_for_user(user_id)
        current_state_str = await get_clean_state_identifier(current_state)
        current_keyboard = state_keyboards[(current_state_str, language)]
        current_reply_messages = state_menus[current_state_str]
        current_reply = await get_message(current_reply_messages, state_messages[current_state_str], language)
        await state.set_state(current_state)
        await message.answer(text=current_reply, reply_markup=current_keyboard, parse_mode="MARKDOWN")
        logger.info(f"User {user_id} passed the captcha and state restored to {current_state_str}.")
    else:
        logger.warning(f"User {message.from_user.id} failed the captcha.")


@state_handler_router.message(RegistrationState.captcha_state)
async def captcha_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает ответ пользователя на капчу в процессе регистрации.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает ответ пользователя на капчу.
    - Проверяет правильность ответа.
    - Если ответ правильный, переводит пользователя в состояние выбора языка.
    """
    logger.debug("Executing captcha_response_handler_in_reg")
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    result = await check_captcha(message)
    if result:
        await state.set_state(RegistrationState.lang_choose_state)
        reply = await get_message(menu_messages, "LANGUAGE_CHOOSE", "ENG")
        await message.answer(text=reply, reply_markup=language_choose_kb)
        logger.info(f"User {message.from_user.id} passed the captcha and moved to lang_choose_state.")
    else:
        logger.warning(f"User {message.from_user.id} failed the captcha.")


@state_handler_router.message(RegistrationState.lang_choose_state)
async def lang_choose_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает выбор языка пользователем в процессе регистрации.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает выбор языка пользователя.
    - Проверяет правильность выбора языка.
    - Если язык выбран правильно, переводит пользователя в состояние приветствия.
    - Обновляет язык пользователя в базе данных.
    """
    logger.debug("Executing lang_choose_response_handler_in_reg")
    user_response = message.text
    await state.update_data(user_lang_choose_response=user_response)
    user_id = message.from_user.id

    if user_response == "ENG English":
        language = "ENG"
    elif user_response == "RU Русский":
        language = "RU"
    else:
        reply = await get_message(menu_messages, "LANGUAGE_CHOSEN_WRONG", "ENG")
        await message.answer(text=reply, reply_markup=language_choose_kb)
        logger.warning(f"User {user_id} selected an invalid language: {user_response}")
        return

    await state.set_state(RegistrationState.hello_state)
    await set_user_state(user_id, await get_clean_state_identifier(RegistrationState.hello_state))
    welcome_message = await get_message(messages, "WELCOME_MESSAGE", language, user_name=message.from_user.first_name)
    await message.answer(text=welcome_message, reply_markup=join_kb[language], parse_mode="MARKDOWN")
    await update_language_in_db(user_id, language)

    logger.info(f"User {user_id} selected language {language} and moved to hello_state.")


@state_handler_router.message(RegistrationState.hello_state)
async def hello_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает ответ пользователя на приветственное сообщение в процессе регистрации.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает ответ пользователя на приветственное сообщение.
    - Если пользователь согласен присоединиться к аирдропу, переводит его в состояние продолжения регистрации.
    - Если пользователь отказывается, запрашивает подтверждение отказа.
    - В противном случае, повторно отправляет приветственное сообщение.
    """
    logger.debug("Executing hello_response_handler_in_reg")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    await state.update_data(user_hello_response=user_response)

    if user_response in ["🚀Join Airdrop", "🚀Присоединиться к аирдропу"]:
        await state.set_state(RegistrationState.proceed_state)
        await set_user_state(message.from_user.id, await get_clean_state_identifier(RegistrationState.proceed_state))
        reply = await get_message(messages, "PROCEED_MESSAGE", language)
        await message.answer(text=reply, reply_markup=sub_cancel_kb[language], parse_mode="MARKDOWN")
        logger.info(f"User {message.from_user.id} agreed to join the airdrop and moved to proceed_state.")
    elif user_response in ["❌Cancel", "❌Отказаться"]:
        await state.update_data(
            state_end1=CaptchaState.null_state,
            state_end2=RegistrationState.hello_state,
            text1=await get_message(messages, "START_AGAIN_TEXT", language),
            text2=await get_message(messages, "WELCOME_MESSAGE", language, user_name=message.from_user.first_name),
            kb1=kb_start,
            kb2=join_kb[language],
            delete=True
        )
        reply = await get_message(menu_messages, "YES_NO", language)
        await message.answer(text=reply, reply_markup=yes_no_kb[language])
        await state.set_state(RegistrationState.yes_no_state)
        logger.info(f"User {message.from_user.id} chose to cancel. Confirmation requested.")
    else:
        await message.answer(
            text=(await get_message(messages, "WELCOME_MESSAGE", language, user_name=message.from_user.first_name)),
            reply_markup=join_kb[language],
            parse_mode="MARKDOWN")
        logger.warning(f"User {message.from_user.id} provided an invalid response: {user_response}")
        return


@state_handler_router.message(RegistrationState.proceed_state)
async def proceed_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает согласие пользователя с правилами и продолжение регистрации.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает ответ пользователя о согласии с правилами.
    - Если пользователь согласен, переводит его в состояние следования за Telegram каналом.
    - Если пользователь отказывается, запрашивает подтверждение отказа.
    - В противном случае, повторно отправляет сообщение с правилами.
    """
    logger.debug("Executing proceed_response_handler_in_reg")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    await state.update_data(user_proceed_response=user_response)

    if user_response in ["✅Согласен с правилами", "✅Submit Details"]:
        await state.set_state(RegistrationState.follow_telegram_state)
        await set_user_state(message.from_user.id,
                             await get_clean_state_identifier(RegistrationState.follow_telegram_state))
        reply = await get_message(messages, "MAKE_SURE_TELEGRAM", language)
        await message.answer(text=reply, reply_markup=social_join_kb[language])
        logger.info(f"User {message.from_user.id} agreed to the rules and moved to follow_telegram_state.")
    elif user_response in ["❌Cancel", "❌Отказаться"]:
        await state.update_data(
            state_end1=CaptchaState.null_state,
            state_end2=RegistrationState.proceed_state,
            text1=await get_message(messages, "START_AGAIN_TEXT", language),
            text2=await get_message(messages, "PROCEED_MESSAGE", language),
            kb1=kb_start,
            kb2=sub_cancel_kb[language],
            delete=True
        )
        reply = await get_message(menu_messages, "YES_NO", language)
        await message.answer(text=reply, reply_markup=yes_no_kb[language])
        await state.set_state(RegistrationState.yes_no_state)
        logger.info(f"User {message.from_user.id} chose to cancel. Confirmation requested.")
    else:
        reply = await get_message(messages, "PROCEED_MESSAGE", language)
        await message.answer(text=reply, reply_markup=sub_cancel_kb[language], parse_mode="MARKDOWN")
        logger.warning(f"User {message.from_user.id} provided an invalid response: {user_response}")
        return


@state_handler_router.message(RegistrationState.follow_telegram_state)
async def follow_telegram_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает ответ пользователя о вступлении в Telegram канал в процессе регистрации.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает ответ пользователя о вступлении в Telegram канал.
    - Проверяет, действительно ли пользователь вступил в канал.
    - Если да, переводит пользователя в состояние ввода адреса.
    - Если нет, просит пользователя вступить в канал.
    - В случае неизвестной команды, отправляет сообщение с инструкцией.
    """
    logger.debug("Executing follow_telegram_response_handler_in_reg")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    await state.update_data(user_follow_telegram_response=user_response)

    if user_response in ["✅Вступил", "✅Joined"]:
        if await check_joined_telegram_channel(message.from_user.id):
            logger.info(f"User {message.from_user.id} is in all required Telegram channels.")
            await state.set_state(RegistrationState.submit_address_state)
            await set_user_state(message.from_user.id,
                                 await get_clean_state_identifier(RegistrationState.submit_address_state))
            reply = await get_message(messages, "SUBMIT_ADDRESS_TEXT", language)
            await message.answer(text=reply, reply_markup=types.ReplyKeyboardRemove(), parse_mode="MARKDOWN")
        else:
            logger.warning(f"User {message.from_user.id} is not in all required Telegram channels.")
            await state.set_state(RegistrationState.follow_telegram_state)
            reply = await get_message(messages, "NOT_SUB_AT_GROUP_TEXT", language)
            await message.answer(text=reply, reply_markup=social_join_kb[language])
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply, reply_markup=social_join_kb[language])
        await state.set_state(RegistrationState.follow_telegram_state)
        logger.warning(f"User {message.from_user.id} provided an unknown command: {user_response}")


@state_handler_router.message(RegistrationState.submit_address_state)
async def submit_address_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает ответ пользователя с крипто-адресом в процессе регистрации.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает крипто-адрес пользователя.
    - Проверяет валидность и уникальность адреса.
    - Если адрес валидный и уникальный, завершает регистрацию и добавляет пользователя в основное меню.
    - Если адрес уже используется, просит ввести другой адрес.
    - Если адрес невалидный, просит ввести валидный адрес.
    """
    logger.debug("Executing submit_address_response_handler_in_reg")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    await state.update_data(user_submit_address_response=user_response)

    if await check_wallet_exists(user_response):
        if is_valid_crypto_address(user_response):
            logger.info(f"Valid crypto address provided by user {message.from_user.id}.")
            await update_user_details(message.from_user.id, ADDR=user_response, NUM_OF_REFS=0, REF_POINTS=0,
                                      POINTS=AIRDROP_AMOUNT)
            await state.set_state(RegistrationState.main_menu_state)
            await set_user_state(message.from_user.id,
                                 await get_clean_state_identifier(RegistrationState.main_menu_state))
            ref_link = await get_refferal_link(message.from_user.id)
            reply = await get_message(messages, "JOINED_TEXT", language, referral_link=ref_link)
            await message.answer(text=reply, reply_markup=menu_kb[language], parse_mode="MARKDOWN")
            refferer = await get_referrer(message.from_user.id)
            if refferer is not None:
                await increment_referrer_count(refferer)
        else:
            logger.warning(f"Invalid crypto address provided by user {message.from_user.id}.")
            await state.set_state(RegistrationState.submit_address_state)
            reply = await get_message(messages, "INVALID_ADDRESS_TEXT", language)
            await message.answer(text=reply)
    else:
        logger.warning(f"Crypto address already registered for user {message.from_user.id}.")
        await state.set_state(RegistrationState.submit_address_state)
        reply = await get_message(messages, "ADDRESS_ALREADY_REGISTERED_TEXT", language)
        await message.answer(text=reply)


@state_handler_router.message(RegistrationState.main_menu_state)
async def main_menu_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команды пользователя в основном меню.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Определяет команду пользователя в основном меню.
    - Выполняет соответствующие действия, такие как показ профиля, баланса, задач и т.д.
    - Обновляет состояние пользователя и отправляет соответствующее сообщение.
    """
    user_response = message.text
    user = await get_user_details(message.from_user.id)
    logger.debug(f"Handling main menu command, user response {user_response}, user {message.from_user.id}")
    language = await get_language_for_user(message.from_user.id)

    if user_response in ["😈Профиль", "😈Profile"]:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        num_of_refs = user.get("NUM_OF_REFS", 0)
        user_address = user.get("ADDR", "Not provided")
        user_twi = user.get("TWITTER_USER", "Not provided")
        reply = await get_message(menu_messages, "PROFILE_MENU", language, user_name=user_name,
                                  refferal_number=num_of_refs,
                                  address=user_address, user_twitter_link=user_twi, user_id=user_id)
        await message.answer(text=reply, reply_markup=menu_kb[language], parse_mode="MARKDOWN")
        return
    elif user_response in ["#️⃣Информация", "#️⃣Information"]:
        reply = await get_message(menu_messages, "INFORMATION_TEXT", language)
        await message.answer(text=reply, reply_markup=menu_kb[language], parse_mode="MARKDOWN")
        return
    elif user_response in ["👥Пригласить друга", "👥Invite Friends"]:
        ref_link = await get_refferal_link(message.from_user.id)
        reply = await get_message(menu_messages, "INVITE_FRIENDS_TEXT", language, referral_link=ref_link)
        await message.answer(text=reply, reply_markup=menu_kb[language], parse_mode="MARKDOWN")
        return
    elif user_response in ["💰Баланс", "💰Balance"]:
        balance = user.get("POINTS", 0)
        balance_by_refs = user.get("REF_POINTS", 0)
        reply = await get_message(menu_messages, "BALANCE_TEXT", language, balance=balance,
                                  user_referral_balance=balance_by_refs)
        await message.answer(text=reply, reply_markup=menu_kb[language], parse_mode="MARKDOWN")
    elif user_response in ["🥇Задачи", "🥇Tasks"]:
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        task_done_points = await calculate_total_points(tasks_done)
        tasks_total_points = await get_all_points()
        tasks_await = user.get("TASKS_AWAIT", [])
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        reply = await get_message(task_menu_messages, "CHOOSE_NUMBER_TASK_TEXT", language,
                                  tasks_done_points=task_done_points,
                                  tasks_total_points=tasks_total_points)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
    elif user_response in ["🔒Токеномика", "🔒Tokenomics"]:
        reply = await get_message(menu_messages, "TOKENOMICS_TEXT", language)
        await message.answer_photo(caption=reply, photo=types.FSInputFile(path="settings/image/tokenomic.jpg"),
                                   reply_markup=menu_kb[language],
                                   parse_mode="HTML")
        return
    elif user_response in ["🔧Настройки", "🔧Settings"]:
        reply = await get_message(menu_messages, "MENU_SETTINGS", language)
        await message.answer(text=reply, reply_markup=kb_menu_settings[language])
        await state.set_state(RegistrationState.menu_settings)
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply, reply_markup=menu_kb[language])
        return


@state_handler_router.message(RegistrationState.menu_settings)
async def menu_settings(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команды пользователя в меню настроек.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Определяет команду пользователя в меню настроек.
    - Выполняет соответствующие действия, такие как смена языка, удаление аккаунта, смена адреса и т.д.
    - Обновляет состояние пользователя и отправляет соответствующее сообщение.
    """
    user_response = message.text
    logger.debug("Handling menu settings")
    language = await get_language_for_user(message.from_user.id)

    if user_response in ["🌏Сменить Язык", "🌏Change Language"]:
        reply = await get_message(menu_messages, "LANGUAGE_CHOOSE", language)
        await message.answer(text=reply, reply_markup=language_choose_kb)
        await state.set_state(RegistrationState.lang_choose_state_again)
    elif user_response in ["❌Удалить Аккаунт", "❌Delete Account"]:
        await state.update_data(
            state_end1=CaptchaState.null_state,
            state_end2=RegistrationState.menu_settings,
            text1=await get_message(messages, "START_AGAIN_TEXT", language),
            text2=await get_message(menu_messages, "MENU_SETTINGS", language),
            kb1=kb_start,
            kb2=kb_menu_settings[language],
            delete=True
        )
        reply = await get_message(menu_messages, "YES_NO", language)
        await message.answer(text=reply, reply_markup=yes_no_kb[language])
        await state.set_state(RegistrationState.yes_no_state)
    elif user_response in ["⏪Вернуться Назад", "⏪Return back"]:
        await state.set_state(RegistrationState.main_menu_state)
        reply = await get_message(menu_messages, "MENU", language)
        await message.answer(text=reply, reply_markup=menu_kb[language])
    elif user_response in ["🔀Сменить адрес", "🔀Change address"]:
        await state.set_state(RegistrationState.change_address_state)
        await state.update_data(
            state_end1=RegistrationState.change_address_state,
            state_end2=RegistrationState.menu_settings,
            text1=await get_message(menu_messages, "GET_ADDRESS_TEXT", language),
            text2=await get_message(menu_messages, "MENU_SETTINGS", language),
            kb1=kb_tasks_back[language],
            kb2=kb_menu_settings[language],
            delete=False
        )
        reply = await get_message(menu_messages, "CHANGE_ADDRESS_TEXT", language)
        await message.answer(text=reply, reply_markup=yes_no_kb[language])
        await state.set_state(RegistrationState.yes_no_state)
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply, reply_markup=kb_menu_settings[language])
        return


@state_handler_router.message(RegistrationState.lang_choose_state_again)
async def lang_choose_response_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает выбор языка пользователем в меню настроек.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает выбор языка пользователя.
    - Проверяет правильность выбора языка.
    - Если язык выбран правильно, обновляет язык пользователя в базе данных и возвращает в меню настроек.
    """
    logger.debug("Handling language choice response")
    user_response = message.text
    await state.update_data(user_lang_choose_response=user_response)
    user_id = message.from_user.id
    if user_response == "ENG English":
        language = "ENG"
    elif user_response == "RU Русский":
        language = "RU"
    else:
        reply = await get_message(menu_messages, "LANGUAGE_CHOSEN_WRONG", "ENG")
        await message.answer(text=reply, reply_markup=language_choose_kb)
        return
    reply = await get_message(menu_messages, "MENU_SETTINGS", language)
    await message.answer(text=reply, reply_markup=kb_menu_settings[language])
    await state.set_state(RegistrationState.menu_settings)
    await update_language_in_db(user_id, language)


@state_handler_router.message(RegistrationState.yes_no_state)
async def yes_no_reply(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает ответ пользователя на вопрос "Да/Нет".

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает ответ пользователя на вопрос "Да/Нет".
    - В зависимости от ответа выполняет соответствующие действия (удаление аккаунта, возврат в предыдущее состояние).
    - Обновляет состояние пользователя и отправляет соответствующее сообщение.
    """
    logger.debug("Handling yes/no reply")
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
    language = await get_language_for_user(message.from_user.id)
    if user_response in ["Да", "Yes"]:
        if delete:
            refferer = await get_referrer(message.from_user.id)
            if refferer is not None:
                await decrement_referrer_count(refferer)
            await delete_user_from_db(message.from_user.id)
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
        reply = await get_message(menu_messages, "YES_NO", language)
        await message.answer(text=reply, reply_markup=yes_no_kb[language])


@state_handler_router.message(CaptchaState.null_state)
async def null_state(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает состояние нулевой капчи.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Проверяет, существует ли пользователь в базе данных.
    - Если пользователь существует, генерирует капчу и переводит в состояние ожидания капчи.
    - Если пользователь не существует, добавляет его в базу данных, обрабатывает реферера и генерирует капчу.
    - Отправляет пользователю соответствующее сообщение.
    """
    logger.debug("Handling null state")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    if language is None:
        language = "ENG"
    if user_response.lower() in ["start", "начать", r"\начать", r"\start"]:
        if await check_is_user_already_here(message.from_user.id):
            logger.debug(f"User {message.from_user.id} already in db")
            await generate_captcha(message)
            await state.set_state(CaptchaState.wait_captcha_state)
            capture_message = await get_message(messages, "CAPTCHA_MESSAGE", language)
            await message.answer(text=capture_message, reply_markup=types.ReplyKeyboardRemove())
        else:
            logger.debug(f"User {message.from_user.id} not in db")
            await add_user_to_db(message.from_user.id)
            referrer = await get_refferer_id(message.text)
            if referrer is not None:
                await add_referrer_to_user(message.from_user.id, referrer)
            await generate_captcha(message)
            await state.set_state(RegistrationState.captcha_state)
            capture_message = await get_message(messages, "CAPTCHA_MESSAGE", language)
            await message.answer(text=capture_message, reply_markup=types.ReplyKeyboardRemove())
    else:
        reply = await get_message(messages, "START_AGAIN_TEXT", language)
        await message.answer(text=reply, reply_markup=kb_start)
        return


@state_handler_router.message(TasksState.current_tasks_state)
async def current_tasks_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команды пользователя в состоянии текущих задач.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает команду пользователя в состоянии текущих задач.
    - Проверяет выполнение или ожидание задачи.
    - Если задача выполнена или в ожидании, отправляет соответствующее сообщение.
    - Если задача новая, отправляет информацию о задаче.
    - Обновляет состояние пользователя и отправляет соответствующее сообщение.
    """
    logger.debug(f"def current_tasks_handler, task #{message.text}")
    language = await get_language_for_user(message.from_user.id)
    user_response = message.text
    index_task = await get_index_by_text_task(user_response, language)
    logger.debug(f"index task == {index_task}")
    user = await get_user_details(message.from_user.id)
    tasks_done = user.get("TASKS_DONE", [])
    tasks_await = user.get("TASKS_AWAIT", [])
    if index_task is not None and index_task in tasks_done:
        reply1 = await get_message(task_menu_messages, "TASK_DONE_ALREADY", language)
        total_buttons = await get_num_of_tasks()
        task_done_points = await calculate_total_points(tasks_done)
        tasks_total_points = await get_all_points()
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        reply2 = await get_message(task_menu_messages, "CHOOSE_NUMBER_TASK_TEXT", language,
                                   tasks_done_points=task_done_points,
                                   tasks_total_points=tasks_total_points)
        await message.answer(text=reply1 + reply2, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
        return
    elif index_task in tasks_await:
        reply1 = await get_message(other_messages, "TASK_ALREADY_SEND_TEXT", language)
        total_buttons = await get_num_of_tasks()
        task_done_points = await calculate_total_points(tasks_done)
        tasks_total_points = await get_all_points()
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        reply2 = await get_message(task_menu_messages, "CHOOSE_NUMBER_TASK_TEXT", language,
                                   tasks_done_points=task_done_points,
                                   tasks_total_points=tasks_total_points)
        await message.answer(text=reply1 + reply2, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
        return
    elif index_task is not None and index_task in range(await get_num_of_tasks()):
        reply = await get_message(task_menu_messages, "TASK_DONE_BACK_TEXT", language)
        await message.answer(text=reply, reply_markup=kb_task_done_back[language])
        await state.update_data(num_of_task=user_response)
        await send_task_info(message, index_task)
        await state.set_state(TasksState.single_task_state)
    elif user_response in ["⏪Вернуться Назад", "⏪Return Back"]:
        await state.set_state(RegistrationState.main_menu_state)
        reply = await get_message(menu_messages, "MENU", language)
        await message.answer(text=reply, reply_markup=menu_kb[language], parse_mode="MARKDOWN")
    elif user_response in ["🏆Достижения", "🏆Achievements"]:
        await state.set_state(TasksState.achievements_state)
        user = await get_user_details(message.from_user.id)
        tasks_done = user.get("TASKS_DONE", [])
        points_done = await calculate_total_points(tasks_done)
        reply = await get_message(task_menu_messages, "ACHIEVEMENTS", language, tasks_done=len(tasks_done),
                                  points_done=points_done)
        await message.answer(text=reply, reply_markup=kb_tasks_back[language], parse_mode="MARKDOWN")
    elif user_response in ["📋Все Задания", "📋All Tasks"]:
        await send_all_tasks_info(message, tasks_done)
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        task_done_points = await calculate_total_points(tasks_done)
        tasks_total_points = await get_all_points()
        tasks_await = user.get("TASKS_AWAIT", [])
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        reply = await get_message(task_menu_messages, "CHOOSE_NUMBER_TASK_TEXT", language,
                                  tasks_done_points=task_done_points,
                                  tasks_total_points=tasks_total_points)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        return
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        user = await get_user_details(message.from_user.id)
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_await = user.get("TASKS_AWAIT", [])
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        return


@state_handler_router.message(TasksState.single_task_state)
async def single_task_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команды пользователя в состоянии выполнения одиночной задачи.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает команду пользователя в состоянии выполнения одиночной задачи.
    - Проверяет защиту задачи (скриншот, Twitter, пазл и т.д.).
    - Если задача выполнена, добавляет очки пользователю и отмечает задачу как выполненную.
    - Если требуется защита, переводит в соответствующее состояние для проверки.
    - Обновляет состояние пользователя и отправляет соответствующее сообщение.
    """
    logger.debug(f"def single_task_handler")
    language = await get_language_for_user(message.from_user.id)
    user = await get_user_details(message.from_user.id)
    user_response = message.text
    task_text = await state.get_data()
    index_task = await get_index_by_text_task(task_text["num_of_task"], language)
    if user_response in ["✅Выполнил", "✅Done"]:
        protection = await get_protection_from_task(index_task)
        if not await get_protection_from_task(index_task):
            points = await get_points_from_task(index_task)
            await add_points_to_user(message.from_user.id, points)
            task_marked = await mark_task_as_done(message.from_user.id, index_task)
            tasks_done = user.get("TASKS_DONE", [])
            if task_marked:
                tasks_done.append(index_task)
            task_done_points = await calculate_total_points(tasks_done)
            total_buttons = await get_num_of_tasks()
            tasks_await = user.get("TASKS_AWAIT", [])
            tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
            tasks_total_points = await get_all_points()
            reply = await get_message(task_menu_messages, "CHOOSE_NUMBER_TASK_TEXT", language,
                                      tasks_done_points=task_done_points, tasks_total_points=tasks_total_points)
            await message.answer(text=reply, reply_markup=tasks_keyboard)
            await state.set_state(TasksState.current_tasks_state)
        else:
            if protection == "screen_check":
                reply = await get_message(other_messages, "SEND_PIC_TO_CHECK_TEXT", language)
                await message.answer(text=reply)
                await state.set_state(TasksState.screen_check_state)
            elif protection == "twitter_screen_check":
                reply = await get_message(task_menu_messages, "TYPE_TWITTER_TEXT", language)
                await message.answer(text=reply, parse_mode="MARKDOWN")
                await state.set_state(TasksState.follow_twitter_state)
            elif protection == "puzzle":
                reply = await get_message(other_messages, "PUZZLE_CHECK", language)
                await message.answer(text=reply, reply_markup=kb_tasks_back[language])
                await state.set_state(TasksState.puzzle_check_state)
            else:
                logger.warning(f"THIS PROTECTION IS NOT IMPLEMENTED YET")
                reply = await get_message(other_messages, "PROTECTION_NOT_IMPLEMENTED", language)
                await message.answer(text=reply)
                await state.set_state(TasksState.screen_check_state)
                tasks_done = user.get("TASKS_DONE", [])
                total_buttons = await get_num_of_tasks()
                tasks_await = user.get("TASKS_AWAIT", [])
                tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
                reply = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
                await message.answer(text=reply, reply_markup=tasks_keyboard)
                await state.set_state(TasksState.current_tasks_state)
    elif user_response in ["⏪Вернуться Назад", "⏪Return Back"]:
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_await = user.get("TASKS_AWAIT", [])
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        reply = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply, reply_markup=kb_task_done_back[language])
        return


@state_handler_router.message(TasksState.follow_twitter_state)
async def follow_twitter_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает ответ пользователя на запрос на подписку в Twitter в процессе регистрации.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает ответ пользователя на запрос подписки в Twitter.
    - Проверяет валидность ссылки на Twitter.
    - Если пользователь подписан на канал, обновляет данные пользователя и переводит его в состояние проверки скриншота.
    - Если пользователь уже подписан, возвращает его в меню задач.
    - Если ссылка на Twitter невалидна, возвращает пользователя в меню задач.
    """
    logger.debug("def follow_twitter_response_handler")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    await state.update_data(user_follow_twitter_response=user_response)
    if is_valid_twitter_link(user_response):
        if await check_joined_twitter_channel(user_response):
            logger.info("User has joined the Twitter channel")
            await update_user_details(message.from_user.id, TWITTER_USER=user_response)
            reply = await get_message(other_messages, "SEND_TWITTER_CHECK", language, parse_mode="MARKDOWN")
            await message.answer(text=reply)
            await state.set_state(TasksState.screen_check_state)
        else:
            logger.info("User is already in the database")
            user = await get_user_details(message.from_user.id)
            reply1 = await get_message(messages, "TWITTER_ALREADY_REGISTERED_TEXT", language)
            tasks_done = user.get("TASKS_DONE", [])
            total_buttons = await get_num_of_tasks()
            tasks_await = user.get("TASKS_AWAIT", [])
            tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
            reply2 = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
            await message.answer(text=reply1 + '\n' + reply2, reply_markup=tasks_keyboard)
            await state.set_state(TasksState.current_tasks_state)
    else:
        logger.warning("Invalid Twitter Link")
        reply1 = await get_message(messages, "TWITTER_INVALID_LINK_TEXT", language)
        user = await get_user_details(message.from_user.id)
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_await = user.get("TASKS_AWAIT", [])
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        reply2 = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
        await message.answer(text=reply1 + '\n' + reply2, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)


@state_handler_router.message(TasksState.achievements_state)
async def achievements_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команды пользователя в меню достижений.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Проверяет, выбрал ли пользователь команду "Вернуться Назад".
    - Если команда выбрана, возвращает пользователя в меню текущих задач.
    - Если введена неизвестная команда, отправляет сообщение с указанием на неизвестную команду.
    """
    logger.debug("def achievements_handler")
    language = await get_language_for_user(message.from_user.id)
    user_response = message.text
    user = await get_user_details(message.from_user.id)
    if user_response in ["⏪Вернуться Назад", "⏪Return Back"]:
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_await = user.get("TASKS_AWAIT", [])
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        reply = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply, reply_markup=kb_task_done_back[language])
        return


@state_handler_router.message(TasksState.screen_check_state)
async def handle_screen_check(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает проверку скриншотов, отправленных пользователем для выполнения задания.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Получает скриншот от пользователя.
    - Помечает задание как ожидающее проверки.
    - Отправляет скриншот администраторам для проверки и начисления очков.
    - Возвращает пользователя в меню текущих задач, если он выбирает опцию "Вернуться Назад".
    - Если пользователь отправил неверный тип сообщения, запрашивает повторную отправку скриншота.
    """
    user_id = message.from_user.id
    user = await get_user_details(user_id)
    language = await get_language_for_user(message.from_user.id)
    task_text = await state.get_data()
    index_task = await get_index_by_text_task(task_text["num_of_task"], language)
    points = await get_points_from_task(index_task)
    if message.photo:
        screenshot = message.photo[-1]
        await mark_task_as_await(message.from_user.id, index_task)
    elif message.text in ["⏪Вернуться Назад", "⏪Return Back"]:
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_await = user.get("TASKS_AWAIT", [])
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        reply = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
        return
    else:
        reply = await get_message(other_messages, "SEND_PIC_TO_CHECK_TEXT", language)
        await message.answer(text=reply)
        await state.set_state(TasksState.screen_check_state)
        return
    if screenshot:
        inline_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да",
                                  callback_data=f"approve_{user_id}_{index_task}_{points}")],
            [InlineKeyboardButton(text="❌ Нет",
                                  callback_data=f"reject_{user_id}_{index_task}")]
        ])
        admin_messages = {}
        for admin_id in ADMINS_IDS:
            if not admin_id:
                logger.debug(f"Пропущен пустой ID администратора: {admin_id}")
                continue
            try:
                admin_id_int = int(admin_id)
                sent_message = await message.bot.send_photo(
                    chat_id=admin_id_int,
                    photo=screenshot.file_id,
                    caption=f"Пользователь {user_id} отправил скриншот для задания {index_task}."
                            f" Начислить {points} очков?"
                )
                await message.bot.edit_message_reply_markup(chat_id=admin_id_int, message_id=sent_message.message_id,
                                                            reply_markup=inline_kb)
                admin_messages[admin_id_int] = sent_message.message_id
            except ValueError:
                logger.error(f"Некорректный ID администратора: {admin_id}")
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение администратору с ID {admin_id}: {e}")
        await insert_admin_messages({index_task: admin_messages}, user_id)
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_await = user.get("TASKS_AWAIT", [])
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        reply = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        reply2 = await get_message(other_messages, "YOUR_PIC_SEND_TEXT", language)
        await message.answer(text=reply2, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
        asyncio.create_task(auto_reject_task(user_id, index_task, admin_messages, message, 36000))
    else:
        reply = await get_message(other_messages, "PLS_SEND_PIC_TEXT", language)
        await message.answer(text=reply)


async def auto_reject_task(user_id: int, index_task: int, admin_messages: dict, message, delay: int) -> None:
    """
    Автоматически отклоняет задание, если оно не было проверено в течение заданного времени.

    Параметры:
    - user_id (int): Идентификатор пользователя.
    - index_task (int): Индекс задания.
    - admin_messages (dict): Словарь с сообщениями администраторов, ожидающих проверки.
    - message: Сообщение, инициировавшее проверку задания.
    - delay (int): Задержка в секундах перед автоматическим отклонением задания.

    Действия:
    - Ждет указанное время (delay).
    - Проверяет, находится ли задание в списке ожидающих.
    - Удаляет задание из списка ожидающих.
    - Удаляет сообщения администраторов, связанные с этим заданием.
    - Отправляет пользователю сообщение о необходимости повторной попытки выполнения задания.
    """
    await asyncio.sleep(delay)
    user = await get_user_details(user_id)
    tasks_await = user.get("TASKS_AWAIT", [])
    if index_task in tasks_await:
        await remove_task_from_await(user_id, index_task)
        if index_task in admin_messages:
            await delete_admin_message(index_task, user_id)
        user_language = await get_language_for_user(user_id)
        reply = await get_message(other_messages, "TRY_AGAIN_TEXT", user_language)
        await message.answer(text=reply)
        logger.info(f"Task {index_task} rejected for user {user_id} due to timeout")


@state_handler_router.callback_query(lambda callback_query: callback_query.data.startswith("approve_"))
async def approve_task(callback_query: types.CallbackQuery) -> None:
    """
    Обрабатывает одобрение задания администратором.

    Параметры:
    - callback_query (types.CallbackQuery): Объект входящего callback запроса.

    Действия:
    - Проверяет, имеет ли пользователь права администратора.
    - Извлекает данные из callback запроса.
    - Получает сообщения администраторов и данные о пользователе.
    - Если задание все еще ожидает проверки, удаляет его из списка ожидающих, добавляет очки и отмечает как выполненное.
    - Отправляет пользователю сообщение об успешном выполнении задания.
    - Если задание больше не ожидает проверки, удаляет сообщения администраторов.
    """
    admin_user_id = callback_query.from_user.id
    language = await get_language_for_user(admin_user_id)
    if callback_query.from_user.id not in ADMINS_IDS:
        reply = await get_message(other_messages, "NO_PERMISSION_TEXT", language)
        await callback_query.answer(text=reply)
        return
    data = callback_query.data.split("_")
    user_id = int(data[1])
    index_task = int(data[2])
    points = int(data[3])
    admin_messages_dict = await get_admin_messages_dict(user_id)
    admin_messages = admin_messages_dict.get(index_task, {})
    user = await get_user_details(user_id)
    tasks_await = user.get("TASKS_AWAIT", [])
    if index_task in tasks_await:
        await remove_task_from_await(user_id, index_task)
        for admin_id, message_id in admin_messages.items():
            try:
                await callback_query.message.bot.delete_message(chat_id=admin_id, message_id=message_id)
            except Exception as e:
                logger.error(f"Failed to delete message {message_id} for admin {admin_id}: {e}")
        if index_task in admin_messages_dict:
            await delete_admin_message(index_task, user_id)
        task_done = user.get("TASKS_DONE", [])
        if index_task not in task_done:
            await add_points_to_user(user_id, points)
            await mark_task_as_done(user_id, index_task)
        user_language = user.get("LANGUAGE", "")
        reply = await get_message(other_messages, "TASK_DONE_TEXT", user_language, index_task=index_task + 1)
        await callback_query.message.bot.send_message(chat_id=user_id, text=reply)
        reply2 = await get_message(other_messages, "TASK_CONFIRMED_TEXT", user_language)
        await callback_query.answer(text=reply2)
    else:
        logger.info("Tasks not in task_await, delete")
        for admin_id, message_id in admin_messages.items():
            try:
                await callback_query.message.bot.delete_message(chat_id=admin_id, message_id=message_id)
            except Exception as e:
                logger.error(
                    f"Failed to delete message {message_id} for admin {admin_id}: {e} (task not in task_await)")
        if index_task in admin_messages_dict:
            await delete_admin_message(index_task, user_id)


@state_handler_router.callback_query(lambda callback_query: callback_query.data.startswith("reject_"))
async def reject_task(callback_query: types.CallbackQuery) -> None:
    """
    Обрабатывает запрос на одобрение задания администратором.

    Параметры:
    - callback_query (types.CallbackQuery): Объект входящего запроса обратного вызова.

    Действия:
    - Проверяет, является ли пользователь администратором.
    - Извлекает данные из запроса.
    - Удаляет задание из списка ожидающих заданий.
    - Удаляет сообщения администраторов, связанные с этим заданием.
    - Начисляет очки пользователю за выполнение задания.
    - Отправляет пользователю сообщение о успешном выполнении задания.
    - Отправляет администратору подтверждение о выполнении задания.
    """
    admin_user_id = callback_query.from_user.id
    language = await get_language_for_user(admin_user_id)
    if callback_query.from_user.id not in ADMINS_IDS:
        reply = await get_message(other_messages, "NO_PERMISSION_TEXT", language)
        await callback_query.answer(text=reply)
        return
    data = callback_query.data.split("_")
    user_id = int(data[1])
    index_task = int(data[2])
    admin_messages_dict = await get_admin_messages_dict(user_id)
    admin_messages = admin_messages_dict.get(index_task, {})
    user = await get_user_details(user_id)
    tasks_await = user.get("TASKS_AWAIT", [])
    protection = await get_protection_from_task(index_task)
    if protection == "twitter_screen_check":
        await update_user_details(user_id, TWITTER_USER=None)
    if index_task in tasks_await:
        await remove_task_from_await(user_id, index_task)
        for admin_id, message_id in admin_messages.items():
            try:
                await callback_query.message.bot.delete_message(chat_id=admin_id, message_id=message_id)
            except Exception as e:
                logger.error(f"Failed to delete message {message_id} for admin {admin_id}: {e}")
        if index_task in admin_messages_dict:
            await delete_admin_message(index_task, user_id)
        user_language = await get_language_for_user(user_id)
        reply = await get_message(other_messages, "TRY_AGAIN_TEXT", user_language)
        await callback_query.message.bot.send_message(chat_id=user_id, text=reply)
        reply2 = await get_message(other_messages, "TASK_REJECTED_TEXT", user_language)
        await callback_query.answer(text=reply2)
    else:
        logger.info("Tasks not in task_await, delete")
        for admin_id, message_id in admin_messages.items():
            try:
                await callback_query.message.bot.delete_message(chat_id=admin_id, message_id=message_id)
            except Exception as e:
                logger.error(
                    f"Failed to delete message {message_id} for admin {admin_id}: {e} (task not in task_await)")
        if index_task in admin_messages_dict:
            await delete_admin_message(index_task, user_id)


@state_handler_router.message(AdminMessageState.waiting_for_message)
async def handle_admin_message(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение администратора для рассылки всем пользователям.

    Параметры:
    - message (types.Message): Входящее сообщение от администратора.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Проверяет, является ли отправитель администратором.
    - Определяет тип контента сообщения (текст, фото, видео, анимация).
    - Отправляет сообщение всем пользователям.
    - Обновляет состояние конечного автомата.
    """
    user_id = message.from_user.id
    language = await get_language_for_user(user_id)
    if message.from_user.id not in ADMINS_IDS:
        reply = await get_message(other_messages, "NO_PERMISSION_TEXT", language)
        await message.answer(text=reply)
        return
    content_type = message.content_type
    user_message = message.text if content_type == types.ContentType.TEXT else (message.caption or "")
    if content_type == types.ContentType.TEXT:
        reply = await get_message(other_messages, "SEND_MESSAGE_TEXT", language, message=user_message)
        await message.answer(text=reply)
    elif content_type == types.ContentType.PHOTO:
        reply = await get_message(other_messages, "SEND_PHOTO_TEXT", language)
        await message.answer(text=reply)
    elif content_type == types.ContentType.VIDEO:
        reply = await get_message(other_messages, "SEND_VIDEO_TEXT", language)
        await message.answer(text=reply)
    elif content_type == types.ContentType.ANIMATION:
        reply = await get_message(other_messages, "SEND_GIF_TEXT", language)
        await message.answer(text=reply)
    all_users = await get_all_users()
    for user in all_users:
        try:
            if content_type == types.ContentType.TEXT:
                await message.bot.send_message(chat_id=user["USER_ID"], text=user_message, parse_mode="Markdown")
            elif content_type == types.ContentType.PHOTO:
                photo = message.photo[-1].file_id
                await message.bot.send_photo(chat_id=user["USER_ID"], photo=photo, caption=user_message,
                                             parse_mode="Markdown")
            elif content_type == types.ContentType.VIDEO:
                video = message.video.file_id
                await message.bot.send_video(chat_id=user["USER_ID"], video=video, caption=user_message,
                                             parse_mode="Markdown")
            elif content_type == types.ContentType.ANIMATION:
                animation = message.animation.file_id
                await message.bot.send_animation(chat_id=user["USER_ID"], animation=animation, caption=user_message,
                                                 parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение пользователю с ID {user['USER_ID']}: {e}")
    await state.set_state(RegistrationState.main_menu_state)
    reply = await get_message(other_messages, "MESSAGE_SENT_TEXT", language)
    await message.answer(text=reply)


@state_handler_router.message(RegistrationState.change_address_state)
async def change_address(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает запрос пользователя на изменение адреса криптокошелька.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Проверяет, хочет ли пользователь вернуться назад.
    - Проверяет, существует ли указанный кошелек.
    - Проверяет валидность указанного адреса криптокошелька.
    - Обновляет адрес криптокошелька пользователя.
    - Обрабатывает ошибки и отправляет соответствующие сообщения.
    """
    user_id = message.from_user.id
    language = await get_language_for_user(user_id)
    user_response = message.text
    if user_response in ["⏪Вернуться Назад", "⏪Return Back"]:
        reply = await get_message(menu_messages, "MENU_SETTINGS", language)
        await message.answer(text=reply, reply_markup=kb_menu_settings[language])
        await state.set_state(RegistrationState.menu_settings)
        return
    if await check_wallet_exists(user_response):
        if is_valid_crypto_address(user_response):
            logger.info("Valid crypto address")
            await update_user_details(message.from_user.id, ADDR=user_response)
            reply = await get_message(menu_messages, "SUCCESS_CHANGE_ADRESS", language)
            await message.answer(text=reply, reply_markup=kb_menu_settings[language])
            await state.set_state(RegistrationState.menu_settings)
        else:
            logger.warning("Invalid crypto address")
            await state.set_state(RegistrationState.change_address_state)
            reply = await get_message(messages, "INVALID_ADDRESS_TEXT", language)
            await message.answer(text=reply, reply_markup=kb_tasks_back[language])
            return
    else:
        await state.set_state(RegistrationState.change_address_state)
        reply = await get_message(messages, "ADDRESS_ALREADY_REGISTERED_TEXT", language)
        await message.answer(text=reply, reply_markup=kb_tasks_back[language])
        return


@state_handler_router.message(TasksState.puzzle_check_state)
async def puzzle_check(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает ответ пользователя на задание-головоломку.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Проверяет, хочет ли пользователь вернуться назад.
    - Проверяет ответ пользователя на головоломку.
    - Начисляет очки пользователю, если головоломка решена верно.
    - Отправляет пользователю соответствующие сообщения и обновляет состояние.
    """
    user = await get_user_details(message.from_user.id)
    language = await get_language_for_user(message.from_user.id)
    if message.text in ["⏪Вернуться Назад", "⏪Return Back"]:
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_await = user.get("TASKS_AWAIT", [])
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
        reply = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
        return
    else:
        task_text = await state.get_data()
        index_task = await get_index_by_text_task(task_text["num_of_task"], language)
        points = await get_points_from_task(index_task)
        user_response = message.text
        puzzle = await get_puzzle_from_task(index_task)
        if user_response in puzzle:
            logger.info("Puzzle solved")
            await add_points_to_user(message.from_user.id, points)
            task_marked = await mark_task_as_done(message.from_user.id, index_task)
            tasks_done = user.get("TASKS_DONE", [])
            if task_marked:
                tasks_done.append(index_task)
            task_done_points = await calculate_total_points(tasks_done)
            total_buttons = await get_num_of_tasks()
            tasks_await = user.get("TASKS_AWAIT", [])
            tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done + tasks_await, language)
            tasks_total_points = await get_all_points()
            reply1 = await get_message(other_messages, "CORRECT_ANSWER", language)
            await message.answer(text=reply1)
            reply2 = await get_message(task_menu_messages, "CHOOSE_NUMBER_TASK_TEXT", language,
                                       tasks_done_points=task_done_points, tasks_total_points=tasks_total_points)
            await message.answer(text=reply2, reply_markup=tasks_keyboard)
            await state.set_state(TasksState.current_tasks_state)
        else:
            reply = await get_message(other_messages, "PUZZLE_REJECTED", language)
            await message.answer(text=reply, reply_markup=kb_tasks_back[language])
            await state.set_state(TasksState.puzzle_check_state)
