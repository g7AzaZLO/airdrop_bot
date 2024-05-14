from aiogram import types, Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from FSM.states import CaptchaState, RegistrationState, TasksState
from logic.captcha import generate_captcha, check_captcha
from aiogram.fsm.context import FSMContext
from handlers.standart_handler import get_message
from messages.basic_messages import messages
from messages.menu_messages import menu_messages
from messages.task_menu_messages import task_menu_messages
from keyboards.menu_kb import menu_kb, kb_menu_settings, create_numeric_keyboard
from keyboards.small_kb import join_kb, language_choose_kb, yes_no_kb, sub_cancel_kb, social_join_kb, kb_start, \
    kb_task_done_back, kb_tasks_back
from DB.database_logic import update_language_in_db, get_language_for_user, delete_user_from_db, get_user_details, \
    update_user_details, check_wallet_exists, decrement_referrer_count, mark_task_as_done
from logic.telegram import check_joined_telegram_channel
from DB.database_logic import check_is_user_already_here, add_user_to_db, add_referrer_to_user, get_referrer, \
    increment_referrer_count, add_points_to_user
from logic.refs import get_refferer_id, get_refferal_link
from logic.twitter import check_joined_twitter_channel, is_valid_twitter_link
from logic.address import is_valid_crypto_address
from logic.task import get_all_points, get_num_of_tasks, get_index_by_text_task, get_protection_from_task, \
    calculate_total_points, get_points_from_task, send_task_info
from tasks.task_dict import protection_fot_admins
from settings.config import AIRDROP_AMOUNT, ADMINS_IDS

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
        await state.set_state(RegistrationState.main_menu_state)
        language = await get_language_for_user(message.from_user.id)
        reply = await get_message(menu_messages, "MENU", language)
        await message.answer(text=reply, reply_markup=menu_kb[language])
        if language not in ["ENG", "RU"]:
            await state.set_state(RegistrationState.lang_choose_state)
            reply = await get_message(menu_messages, "LANGUAGE_CHOOSE", "ENG")
            await message.answer(text=reply, reply_markup=language_choose_kb)


# Handler состояния капчи в регистрации пользователя
@state_handler_router.message(RegistrationState.captcha_state)
async def captcha_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def captcha_response_handler_in_reg")
    user_response = message.text
    await state.update_data(user_captcha_response=user_response)
    result = await check_captcha(message)
    if result:
        await state.set_state(RegistrationState.lang_choose_state)
        reply = await get_message(menu_messages, "LANGUAGE_CHOOSE", "ENG")
        await message.answer(text=reply, reply_markup=language_choose_kb)


@state_handler_router.message(RegistrationState.lang_choose_state)
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
        reply = await get_message(menu_messages, "LANGUAGE_CHOSEN_WRONG", "ENG")
        await message.answer(text=reply, reply_markup=language_choose_kb)
        return
    await state.set_state(RegistrationState.hello_state)
    await message.answer(
        text=(await get_message(messages, "WELCOME_MESSAGE", language, user_name=message.from_user.first_name)),
        reply_markup=join_kb[language],
        parse_mode="MARKDOWN")
    # Вызываем функцию для обновления языка пользователя в базе данных
    await update_language_in_db(user_id, language)


@state_handler_router.message(RegistrationState.hello_state)
async def hello_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def hello_response_handler_in_reg")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    await state.update_data(user_hello_response=user_response)
    if user_response in ["🚀Join Airdrop", "🚀Присоединиться к аирдропу"]:
        await state.set_state(RegistrationState.proceed_state)
        reply = await get_message(messages, "PROCEED_MESSAGE", language)
        await message.answer(text=reply, reply_markup=sub_cancel_kb[language], parse_mode="MARKDOWN")
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
    else:
        await message.answer(
            text=(await get_message(messages, "WELCOME_MESSAGE", language, user_name=message.from_user.first_name)),
            reply_markup=join_kb[language],
            parse_mode="MARKDOWN")
        return


@state_handler_router.message(RegistrationState.proceed_state)
async def proceed_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def proceed_response_handler_in_reg")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    await state.update_data(user_proceed_response=user_response)
    if user_response in ["✅Согласен с правилами", "✅Submit Details"]:
        await state.set_state(RegistrationState.follow_telegram_state)
        reply = await get_message(messages, "MAKE_SURE_TELEGRAM", language)
        await message.answer(text=reply, reply_markup=social_join_kb[language])
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
    else:
        reply = await get_message(messages, "PROCEED_MESSAGE", language)
        await message.answer(text=reply, reply_markup=sub_cancel_kb[language], parse_mode="MARKDOWN")
        return


@state_handler_router.message(RegistrationState.follow_telegram_state)
async def follow_telegram_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def follow_telegram_response_handler")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    await state.update_data(user_follow_telegram_response=user_response)
    if user_response in ["✅Вступил", "✅Joined"]:
        if await check_joined_telegram_channel(message.from_user.id):
            print("Yes, user in all telegram channel")
            await state.set_state(RegistrationState.follow_twitter_state)
            reply1 = await get_message(messages, "FOLLOW_TWITTER_TEXT", language)
            reply2 = await get_message(messages, "GET_TWITTER_LINK_TEXT", language)
            await message.answer(text=reply1, reply_markup=types.ReplyKeyboardRemove())
            await message.answer(text=reply2)
        else:
            print("NO HE ISNT HERE")
            await state.set_state(RegistrationState.follow_telegram_state)
            reply = await get_message(messages, "NOT_SUB_AT_GROUP_TEXT", language)
            await message.answer(text=reply, reply_markup=social_join_kb[language])
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply, reply_markup=social_join_kb[language])
        await state.set_state(RegistrationState.follow_telegram_state)


@state_handler_router.message(RegistrationState.follow_twitter_state)
async def follow_twitter_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def follow_twitter_response_handler")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    await state.update_data(user_follow_twitter_response=user_response)
    if is_valid_twitter_link(user_response):
        if await check_joined_twitter_channel(user_response):
            print("all ok")
            await update_user_details(message.from_user.id, TWITTER_USER=user_response)
            await state.set_state(RegistrationState.submit_address_state)
            reply = await get_message(messages, "SUBMIT_ADDRESS_TEXT", language)
            await message.answer(text=reply, reply_markup=types.ReplyKeyboardRemove(), parse_mode="MARKDOWN")
        else:
            print("already in base")
            await state.set_state(RegistrationState.follow_twitter_state)
            reply = await get_message(messages, "TWITTER_ALREADY_REGISTERED_TEXT", language)
            await message.answer(text=reply)
    else:
        print("Invalid Twitter Link")
        await state.set_state(RegistrationState.follow_twitter_state)
        reply = await get_message(messages, "TWITTER_INVALID_LINK_TEXT", language)
        await message.answer(text=reply)


@state_handler_router.message(RegistrationState.submit_address_state)
async def submit_address_response_handler_in_reg(message: types.Message, state: FSMContext) -> None:
    print("def submit_address_response_handler_in_reg")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    await state.update_data(user_submit_address_response=user_response)
    if await check_wallet_exists(user_response):
        if is_valid_crypto_address(user_response):
            print("Valid crypto address")
            await update_user_details(message.from_user.id, ADDR=user_response, NUM_OF_REFS=0, REF_POINTS=0,
                                      POINTS=AIRDROP_AMOUNT)
            await state.set_state(RegistrationState.main_menu_state)
            ref_link = await get_refferal_link(message.from_user.id)
            reply = await get_message(messages, "JOINED_TEXT", language, referral_link=ref_link)
            await message.answer(text=reply, reply_markup=menu_kb[language], parse_mode="MARKDOWN")
            refferer = await get_referrer(message.from_user.id)
            if refferer is not None:
                await increment_referrer_count(refferer)
        else:
            print("Invalid crypto address")
            await state.set_state(RegistrationState.submit_address_state)
            reply = await get_message(messages, "INVALID_ADDRESS_TEXT", language)
            await message.answer(text=reply)
    else:
        await state.set_state(RegistrationState.submit_address_state)
        reply = await get_message(messages, "ADDRESS_ALREADY_REGISTERED_TEXT", language)
        await message.answer(text=reply)


@state_handler_router.message(RegistrationState.main_menu_state)
async def main_menu_handler(message: types.Message, state: FSMContext) -> None:
    user_response = message.text
    user = await get_user_details(message.from_user.id)
    print(f"def main_menu_handler, user response {user_response}, user {message.from_user.id}")
    language = await get_language_for_user(message.from_user.id)
    if user_response in ["😈Профиль", "😈Profile"]:

        user_name = message.from_user.first_name
        num_of_refs = user.get("NUM_OF_REFS", 0)
        user_address = user.get("ADDR", "Not provided")
        user_twi = user.get("TWITTER_USER", "Not provided")
        reply = await get_message(menu_messages, "PROFILE_MENU", language, user_name=user_name,
                                  refferal_number=num_of_refs,
                                  address=user_address, user_twitter_link=user_twi)
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
        # reply = await get_message(menu_messages, "INFORMATION_TEXT", language)
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        task_done_points = await calculate_total_points(tasks_done)
        tasks_total_points = await get_all_points()
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done, language)
        reply = await get_message(task_menu_messages, "CHOOSE_NUMBER_TASK_TEXT", language,
                                  tasks_done_points=task_done_points,
                                  tasks_total_points=tasks_total_points)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
    elif user_response in ["🔒Смартконтракт", "🔒Smartcontract"]:
        reply = await get_message(menu_messages, "SMARTCONTRACT_TEXT", language)
        await message.answer(text=reply, reply_markup=menu_kb[language], parse_mode="HTML")
        return
    elif user_response in ["🔧Настройки", "🔧Settings"]:
        reply = await get_message(menu_messages, "MENU_SETTINGS", language)
        await message.answer(text=reply, reply_markup=kb_menu_settings[language])
        await state.set_state(RegistrationState.menu_settings)
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply, reply_markup=menu_kb[language])
        # await state.set_state(RegistrationState.main_menu_state)
        return


@state_handler_router.message(RegistrationState.menu_settings)
async def menu_settings(message: types.Message, state: FSMContext) -> None:
    user_response = message.text
    print(f"def menu_settings")
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
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply, reply_markup=kb_menu_settings[language])
        return


@state_handler_router.message(RegistrationState.lang_choose_state_again)
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
        reply = await get_message(menu_messages, "LANGUAGE_CHOSEN_WRONG", "ENG")
        await message.answer(text=reply, reply_markup=language_choose_kb)
        return
    reply = await get_message(menu_messages, "MENU_SETTINGS", language)
    await message.answer(text=reply, reply_markup=kb_menu_settings[language])
    await state.set_state(RegistrationState.menu_settings)
    # Вызываем функцию для обновления языка пользователя в базе данных
    await update_language_in_db(user_id, language)


@state_handler_router.message(RegistrationState.yes_no_state)
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
    print("def null_state")
    user_response = message.text
    language = await get_language_for_user(message.from_user.id)
    if language is None: language = "ENG"
    if user_response in ["start", "Start", "Начать", "начать",
                         r"\Начать", r"\начать", r"\start", r"\Start", ]:
        if await check_is_user_already_here(message.from_user.id):
            print("User already in db")
            await generate_captcha(message)
            await state.set_state(CaptchaState.wait_captcha_state)
            capture_message = await get_message(messages, "CAPTCHA_MESSAGE", language)
            await message.answer(text=capture_message, reply_markup=types.ReplyKeyboardRemove())
        # Запуск меню после капчи
        else:
            print("User not in db")
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
    print(f"def current_tasks_handler, task #{message.text}")
    # reply = await get_message(menu_messages, "INFORMATION_TEXT", language)
    language = await get_language_for_user(message.from_user.id)
    user_response = message.text
    index_task = await get_index_by_text_task(user_response, language)
    print("index task == " + str(index_task))
    user = await get_user_details(message.from_user.id)
    tasks_done = user.get("TASKS_DONE", [])
    if index_task is not None and index_task in tasks_done:
        reply1 = await get_message(task_menu_messages, "TASK_DONE_ALREADY", language)
        total_buttons = await get_num_of_tasks()
        task_done_points = await calculate_total_points(tasks_done)
        tasks_total_points = await get_all_points()
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done, language)
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
        reply = await get_message(task_menu_messages, "ACHIEVEMENTS", language, tasks_done=tasks_done,
                                  points_done=points_done)
        await message.answer(text=reply, reply_markup=kb_tasks_back[language], parse_mode="MARKDOWN")
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        user = await get_user_details(message.from_user.id)
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done, language)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        return


@state_handler_router.message(TasksState.single_task_state)
async def single_task_handler(message: types.Message, state: FSMContext) -> None:
    print(f"def single_task_handler")
    language = await get_language_for_user(message.from_user.id)
    user = await get_user_details(message.from_user.id)
    user_response = message.text
    task_text = await state.get_data()
    index_task = await get_index_by_text_task(task_text["num_of_task"], language)
    if user_response in ["✅Выполнил", "✅Done"]:
        if await get_protection_from_task(index_task) not in protection_fot_admins:
            points = await get_points_from_task(index_task)
            await add_points_to_user(message.from_user.id, points)
            task_marked = await mark_task_as_done(message.from_user.id, index_task)
            tasks_done = user.get("TASKS_DONE", [])
            if task_marked:
                tasks_done.append(index_task)
            task_done_points = await calculate_total_points(tasks_done)
            total_buttons = await get_num_of_tasks()
            tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done, language)
            tasks_total_points = await get_all_points()
            reply = await get_message(task_menu_messages, "CHOOSE_NUMBER_TASK_TEXT", language,
                                      tasks_done_points=task_done_points, tasks_total_points=tasks_total_points)
            await message.answer(text=reply, reply_markup=tasks_keyboard)
            await state.set_state(TasksState.current_tasks_state)
        else:
            await message.answer(text="Пришлите скриншот для проверки")
            await state.set_state(TasksState.screen_check_state)  # Устанавливаем новое состояние для отправки фото
    elif user_response in ["⏪Вернуться Назад", "⏪Return Back"]:
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done, language)
        reply = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply, reply_markup=kb_task_done_back[language])
        return


@state_handler_router.message(TasksState.achievements_state)
async def achievements_handler(message: types.Message, state: FSMContext) -> None:
    print(f"def achievements_handler")
    language = await get_language_for_user(message.from_user.id)
    user_response = message.text
    user = await get_user_details(message.from_user.id)
    if user_response in ["⏪Вернуться Назад", "⏪Return Back"]:
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done, language)
        reply = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
    else:
        reply = await get_message(menu_messages, "UNKNOWN_COMMAND_TEXT", language)
        await message.answer(text=reply, reply_markup=kb_task_done_back[language])
        return


# TODO все таки нужно убирвть кнопку после отправки задания на проверку, чтобы юзер не мог повторно ничего отправлять пока не пройдет проверка.
# TODO Либо ставить защиту что юзер не может отправить новый скрин пока не проверен старый

# TODO нужно избавиться от двойного отказа двемя разными админами
@state_handler_router.message(TasksState.screen_check_state, F.photo)
async def handle_screen_check(message: types.Message, state: FSMContext) -> None:
    screenshot = message.photo[-1] if message.photo else None
    user_id = message.from_user.id
    task_text = await state.get_data()
    index_task = await get_index_by_text_task(task_text["num_of_task"], await get_language_for_user(user_id))
    points = await get_points_from_task(index_task)
    user = await get_user_details(message.from_user.id)
    language = await get_language_for_user(user_id)
    if screenshot:
        inline_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да", callback_data=f"approve_{user_id}_{index_task}_{points}")],
            [InlineKeyboardButton(text="❌ Нет", callback_data=f"reject_{user_id}_{index_task}")]
        ])
        for admin_id in ADMINS_IDS:
            if not admin_id:
                print(f"Пропущен пустой ID администратора: {admin_id}")
                continue
            try:
                admin_id_int = int(admin_id)
                await message.bot.send_photo(chat_id=admin_id_int, photo=screenshot.file_id,
                                             caption=f"Пользователь {user_id} отправил скриншот для задания {index_task}. Начислить {points} очков?",
                                             reply_markup=inline_kb)
            except ValueError:
                print(f"Некорректный ID администратора: {admin_id}")
            except Exception as e:
                print(f"Не удалось отправить сообщение администратору с ID {admin_id}: {e}")
        tasks_done = user.get("TASKS_DONE", [])
        total_buttons = await get_num_of_tasks()
        tasks_keyboard = await create_numeric_keyboard(total_buttons, tasks_done, language)
        reply = await get_message(task_menu_messages, "WE_ARE_BACK_CHOOSE_TEXT", language)
        await message.answer(text=reply, reply_markup=tasks_keyboard)
        await message.answer("Ваш скриншот отправлен на проверку.", reply_markup=tasks_keyboard)
        await state.set_state(TasksState.current_tasks_state)
    else:
        await message.answer("Пожалуйста, отправьте скриншот.")


@state_handler_router.callback_query(lambda callback_query: callback_query.data.startswith("approve_"))
async def approve_task(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in ADMINS_IDS:
        await callback_query.answer("У вас нет прав для выполнения этого действия.", show_alert=True)
        return

    data = callback_query.data.split("_")
    user_id = int(data[1])
    index_task = int(data[2])
    points = int(data[3])

    # Проверка, было ли задание уже обработано
    task_data = await get_user_details(user_id)
    tasks_done = task_data.get("TASKS_DONE", [])
    if index_task in tasks_done:
        await callback_query.answer("Это задание уже было обработано.", show_alert=True)
        return

    await add_points_to_user(user_id, points)
    await mark_task_as_done(user_id, index_task)
    await callback_query.message.bot.send_message(chat_id=user_id, text="Ваше задание выполнено, очки начислены.")
    await callback_query.answer("Задание подтверждено.", show_alert=True)

    # Удаляем сообщение с кнопками после подтверждения
    await callback_query.message.delete()


@state_handler_router.callback_query(lambda callback_query: callback_query.data.startswith("reject_"))
async def reject_task(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in ADMINS_IDS:
        await callback_query.answer("У вас нет прав для выполнения этого действия.", show_alert=True)
        return

    data = callback_query.data.split("_")
    user_id = int(data[1])
    index_task = int(data[2])

    # Проверка, было ли задание уже обработано
    task_data = await get_user_details(user_id)
    tasks_done = task_data.get("TASKS_DONE", [])
    if index_task in tasks_done:
        await callback_query.answer("Это задание уже было обработано.", show_alert=True)
        return

    await callback_query.message.bot.send_message(chat_id=user_id, text="Ваше задание не выполнено, попробуйте снова.")
    await callback_query.answer("Задание отклонено.", show_alert=True)

    # Удаляем сообщение с кнопками после отказа
    await callback_query.message.delete()
