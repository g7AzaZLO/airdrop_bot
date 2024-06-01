from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from messages.basic_messages import messages
from messages.other_messages import other_messages
from logic.captcha import generate_captcha
from aiogram.fsm.context import FSMContext
from FSM.states import CaptchaState, RegistrationState, AdminMessageState
from DB.database_logic import check_is_user_already_here, add_user_to_db, add_referrer_to_user, get_language_for_user, \
    add_admin, remove_admin, get_user_state
from logic.refs import get_refferer_id
from logic.admins import ADMINS_IDS, update_admins_ids
from DB.get_all_admins import get_all_admins
from tasks.task_dict import update_tasks, change_tasks

standard_handler_router = Router()
garbage_handler_router = Router()


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
        reply = await get_message(other_messages, "NO_PERMISSION_TEXT", language)
        await message.answer(text=reply)
        return
    reply = await get_message(other_messages, "ENTER_MESSAGE_TEXT", language)
    await message.answer(text=reply)
    await state.set_state(AdminMessageState.waiting_for_message)


@standard_handler_router.message(Command("update_admin"), F.chat.type == "private")
async def start_update_admin_command(message: types.Message):
    user_id = message.from_user.id
    language = await get_language_for_user(user_id)
    print(ADMINS_IDS)
    if message.from_user.id not in ADMINS_IDS:
        reply = await get_message(other_messages, "NO_PERMISSION_TEXT", language)
        await message.answer(text=reply)
        return
    await update_admins_ids()
    reply = await get_message(other_messages, "ADMINS_BEEN_UPDATE", language) + str(await get_all_admins())
    await message.answer(text=reply)
    return


@standard_handler_router.message(Command("add_admin"), F.chat.type == "private")
async def start_add_admin_command(message: types.Message):
    user_id = message.from_user.id
    language = await get_language_for_user(user_id)
    print(ADMINS_IDS)
    if message.from_user.id not in ADMINS_IDS:
        reply = await get_message(other_messages, "NO_PERMISSION_TEXT", language)
        await message.answer(text=reply)
        return
    try:
        admin_id = int(message.text.split()[1])
        await add_admin(admin_id)
        reply = await get_message(other_messages, "ADD_ADMIN_TEXT", language, admin_id=admin_id)
        await message.answer(text=reply)
    except (IndexError, ValueError):
        reply = await get_message(other_messages, "INCORRECT_ADD_ADMIN_TEXT", language)
        await message.answer(text=reply)


@standard_handler_router.message(Command("del_admin"), F.chat.type == "private")
async def start_del_admin_command(message: types.Message):
    user_id = message.from_user.id
    language = await get_language_for_user(user_id)
    print(ADMINS_IDS)
    all_admin = await get_all_admins()
    if message.from_user.id not in ADMINS_IDS:
        reply = await get_message(other_messages, "NO_PERMISSION_TEXT", language)
        await message.answer(text=reply)
        return
    try:
        admin_id = int(message.text.split()[1])
    except ValueError:
        reply = await get_message(other_messages, "INCORRECT_DEL_ADMIN_TEXT", language)
        await message.answer(text=reply)
        return
    if admin_id in all_admin:
        try:
            await remove_admin(admin_id)
            reply = await get_message(other_messages, "ADMIN_DEL_SUCCESS", language, admin_id=admin_id)
            await message.answer(text=reply)
        except (IndexError, ValueError):
            reply = await get_message(other_messages, "INCORRECT_DEL_ADMIN_TEXT", language, admin_id=admin_id)
            await message.answer(text=reply)
    else:
        reply = await get_message(other_messages, "ADMINS_NOT_FOUND_TEXT", language, admin_id=admin_id)
        await message.answer(text=reply)


@standard_handler_router.message(Command("admin_info"), F.chat.type == "private")
async def start_admin_info_command(message: types.Message):
    user_id = message.from_user.id
    language = await get_language_for_user(user_id)
    print(ADMINS_IDS)
    if message.from_user.id not in ADMINS_IDS:
        reply = await get_message(other_messages, "NO_PERMISSION_TEXT", language)
        await message.answer(text=reply)
        return
    reply = await get_message(other_messages, "ADMIN_INFO", language)
    await message.answer(text=reply)


@standard_handler_router.message(Command("update_tasks"), F.chat.type == "private")
async def start_change_tasks_command(message: types.Message):
    user_id = message.from_user.id
    language = await get_language_for_user(user_id)
    if message.from_user.id not in ADMINS_IDS:
        reply = await get_message(other_messages, "NO_PERMISSION_TEXT", language)
        await message.answer(text=reply)
        return
    await change_tasks()
    reply = await get_message(other_messages, "TASKS_UPDATED_INFO", language)
    await message.answer(text=reply)


@standard_handler_router.message(Command("get_my_id"), F.chat.type == "private")
async def start_change_tasks_command(message: types.Message):
    await message.answer(text=str(message.from_user.id))


@garbage_handler_router.message(F.chat.type == "private")
async def all_other_text_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await get_user_state(user_id)
    # print(f"I am here, state {current_state}")
    if current_state is None:
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
    await state.set_state(current_state)

#
#
# from DB.mongo import users_collection
# from aiogram import types
# from aiogram.fsm.context import FSMContext
# from aiogram import Dispatcher
#
# async def get_all_user_states():
#     try:
#         users = await users_collection.find({}, {"USER_ID": 1, "STATE": 1, "_id": 0}).to_list(length=None)
#         user_states = [(user["USER_ID"], user["STATE"]) for user in users if "STATE" in user]
#         return user_states
#     except Exception as e:
#         print(f"Error retrieving all user states: {e}")
#         return []
#
#
# async def set_user_state(user_id: int, user_state: str, dispatcher: Dispatcher):
#     # state = FSMContext(dispatcher.storage, chat=user_id, user=user_id)
#     state = dispatcher.current_state(user=user_id)
#     await state.set_state(user_state)
#
#
# async def load_all_user_states(dispatcher: Dispatcher):
#     user_states = await get_all_user_states()
#     for user_id, state in user_states:
#         await set_user_state(user_id, state, dispatcher)

# Call this function on bot startup
