from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from messages.basic_messages import messages
from messages.other_messages import other_messages
from logic.captcha import generate_captcha
from aiogram.fsm.context import FSMContext
from FSM.states import CaptchaState, RegistrationState, AdminMessageState, get_clean_state_identifier, \
    state_keyboards, state_menus, state_messages
from DB.database_logic import check_is_user_already_here, add_user_to_db, add_referrer_to_user, get_language_for_user, \
    add_admin, remove_admin, get_state_for_user
from logic.refs import get_refferer_id
from logic.admins import ADMINS_IDS, update_admins_ids
from DB.get_all_admins import get_all_admins
from tasks.task_dict import change_tasks

standard_handler_router = Router()
garbage_handler_router = Router()


async def get_message(msg: dict, message_key: str, language: str, **kwargs) -> str:
    """
    Retrieve a message based on the key and language,
    formatting it with any provided keyword arguments.
    examples:
        capture_message = get_message(messages, "WELCOME_MESSAGE", "ENG")
        print(capture_message)
        capture_message = get_message(messages, "WELCOME_MESSAGE", "RU", user_name='дурачок')
        print(capture_message)
    """
    defaults = msg.get("default_values", {})
    message_template = msg.get(message_key, {}).get(language)
    if message_template:
        all_kwargs = {**defaults, **kwargs}
        return message_template.format(**all_kwargs)
    else:
        return "Message not available."


@standard_handler_router.message(CommandStart(), F.chat.type == "private")
async def start(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду /start для пользователя. Проверяет, зарегистрирован ли пользователь, и запускает процесс капчи.

    Параметры:
    - message (types.Message): Сообщение, содержащее команду /start.
    - state (FSMContext): Контекст конечного автомата состояний (FSM) для отслеживания состояния пользователя.

    Действия: - Если пользователь уже зарегистрирован, генерирует капчу и устанавливает состояние ожидания ответа
    капчи. - Если пользователь не зарегистрирован, добавляет пользователя в базу данных, обрабатывает реферера (если
    имеется), генерирует капчу и устанавливает состояние капчи. - Отправляет соответствующее сообщение пользователю в
    зависимости от его состояния.
    """
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
async def start_message_command(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает команду /message для администраторов. Проверяет права администратора и устанавливает состояние
    для ожидания ввода сообщения.

    Параметры:
    - message (types.Message): Сообщение, содержащее команду /message.
    - state (FSMContext): Контекст конечного автомата состояний (FSM) для отслеживания состояния пользователя.

    Действия:
    - Проверяет, является ли пользователь администратором.
    - Если пользователь не администратор, отправляет сообщение о недостатке прав.
    - Если пользователь администратор, отправляет сообщение с просьбой ввести сообщение и устанавливает соответствующее
      состояние.
    """
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
async def start_update_admin_command(message: types.Message) -> None:
    """
    Обрабатывает команду /update_admin для обновления списка администраторов. Проверяет права администратора и
    обновляет список администраторов в глобальной переменной.

    Параметры:
    - message (types.Message): Сообщение, содержащее команду /update_admin.

    Действия:
    - Проверяет, является ли пользователь администратором.
    - Если пользователь не администратор, отправляет сообщение о недостатке прав.
    - Если пользователь администратор, обновляет список администраторов и отправляет сообщение с новым списком.
    """
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
async def start_add_admin_command(message: types.Message) -> None:
    """
    Обрабатывает команду /add_admin для добавления нового администратора. Проверяет права текущего пользователя
    и добавляет нового администратора по указанному ID.

    Параметры:
    - message (types.Message): Сообщение, содержащее команду /add_admin и ID нового администратора.

    Действия:
    - Проверяет, является ли текущий пользователь администратором.
    - Если пользователь не администратор, отправляет сообщение о недостатке прав.
    - Если пользователь администратор, добавляет нового администратора по указанному ID и отправляет
      подтверждающее сообщение.
    - Если указан некорректный ID, отправляет сообщение об ошибке.
    """
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
async def start_del_admin_command(message: types.Message) -> None:
    """
    Обрабатывает команду /del_admin для удаления администратора. Проверяет права текущего пользователя и удаляет
    администратора по указанному ID.

    Параметры:
    - message (types.Message): Сообщение, содержащее команду /del_admin и ID удаляемого администратора.

    Действия:
    - Проверяет, является ли текущий пользователь администратором.
    - Если пользователь не администратор, отправляет сообщение о недостатке прав.
    - Если пользователь администратор, удаляет администратора по указанному ID и отправляет подтверждающее сообщение.
    - Если указан некорректный ID или администратор не найден, отправляет сообщение об ошибке.
    """
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
async def start_admin_info_command(message: types.Message) -> None:
    """
    Обрабатывает команду /admin_info для отображения информации о текущих администраторах.
    Проверяет права текущего пользователя и отправляет сообщение с информацией, если пользователь
    является администратором.

    Параметры:
    - message (types.Message): Сообщение, содержащее команду /admin_info.

    Действия:
    - Проверяет, является ли текущий пользователь администратором.
    - Если пользователь не администратор, отправляет сообщение о недостатке прав.
    - Если пользователь администратор, отправляет сообщение с информацией о текущих администраторах.
    """
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
async def start_change_tasks_command(message: types.Message) -> None:
    """
    Обрабатывает команду /update_tasks для обновления задач.
    Проверяет права текущего пользователя и обновляет задачи, если пользователь является администратором.

    Параметры:
    - message (types.Message): Сообщение, содержащее команду /update_tasks.

    Действия:
    - Проверяет, является ли текущий пользователь администратором.
    - Если пользователь не администратор, отправляет сообщение о недостатке прав.
    - Если пользователь администратор, обновляет задачи и отправляет сообщение с подтверждением.
    """
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
async def start_change_tasks_command(message: types.Message) -> None:
    """
    Обрабатывает команду /update_tasks и отвечает с ID пользователя.

    Параметры:
    - message (types.Message): Сообщение, содержащее команду /update_tasks.

    Действия:
    - Отправляет ответное сообщение с ID пользователя.
    """
    await message.answer(text=str(message.from_user.id))


@garbage_handler_router.message(F.chat.type == "private")
async def all_other_text_handler(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает любые другие текстовые сообщения, не относящиеся к определенным командам или состояниям.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - state (FSMContext): Контекст состояния конечного автомата.

    Действия:
    - Проверяет, существует ли пользователь в базе данных.
    - Если пользователь существует, генерирует капчу и переводит в соответствующее состояние.
    - Если пользователь не существует, добавляет его в базу данных, обрабатывает реферера и генерирует капчу.
    - Если текущее состояние пользователя определено, восстанавливает его состояние и отвечает соответствующим сообщением.
    """
    user_id = message.from_user.id
    current_state = await get_state_for_user(user_id)
    if current_state is None:
        if await check_is_user_already_here(user_id):
            print("User already in db")
            await generate_captcha(message)
            await state.set_state(CaptchaState.wait_captcha_state)
            capture_message = await get_message(messages, "CAPTCHA_MESSAGE", "ENG")
            await message.answer(text=capture_message, reply_markup=types.ReplyKeyboardRemove())
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
    else:
        await state.set_state(current_state)
        language = await get_language_for_user(message.from_user.id)
        current_state_str = await get_clean_state_identifier(current_state)
        current_keyboard = state_keyboards[(current_state_str, language)]
        current_reply_messages = state_menus[current_state_str]
        current_reply = await get_message(current_reply_messages, state_messages[current_state_str], language)
        await state.set_state(current_state)
        await message.answer(text=current_reply, reply_markup=current_keyboard, parse_mode="MARKDOWN")
