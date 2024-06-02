from aiogram import types, Router
from DB.database_logic import get_language_for_user, get_user_details
from tasks.task_dict import tasks
from handlers.standart_handler import get_message
from messages.other_messages import other_messages

task_router = Router()


async def get_all_points() -> int:
    """
    Возвращает общее количество очков за все существующие задания.

    Возвращает:
    - int: Общее количество очков за все существующие задания.
    """
    print("def get_all_points")
    point_counter = 0
    for task in tasks:
        point_counter += tasks[task]["points"]
    return point_counter


async def get_protection_from_task(index_task: int) -> str:
    """
    Возвращает название защиты задания.

    Параметры:
    - index_task (int): Индекс задания.

    Возвращает:
    - str: название защиты задания
    """
    # index_task -= 1
    print("def get_protection_from_task")
    value_at_index = list(tasks.values())[index_task]
    print(value_at_index)
    return value_at_index["protection"]


async def get_points_from_task(index_task: int) -> int:
    """
    Возвращает количество поинтов за задание.

    Параметры:
    - index_task (int): Индекс задания.

    Возвращает:
    - int: количество поинтов за задание
    """
    print("def get_points_from_task")
    value_at_index = list(tasks.values())[index_task]
    print(value_at_index)
    return value_at_index["points"]


# Функция для вычисления общего количества очков за выполненные задания
async def calculate_total_points(done_tasks: list) -> int:
    """
    Вычисляет общее количество очков за выполненные задания.

    Параметры:
    - done_tasks (list): Список индексов выполненных заданий.

    Возвращает:
    - int: Общее количество очков за все выполненные задания.
    """
    print("calculate_total_points")
    total_points = 0
    for index in done_tasks:
        value_at_index = list(tasks.values())[index]
        if value_at_index:
            total_points += value_at_index["points"]
    return total_points


async def get_num_of_tasks() -> int:
    """
    Возвращает количество существующих заданий.

    Возвращает:
    - int: Количество существующих заданий.
    """
    print("def get_num_of_tasks")
    print(len(tasks))
    return len(tasks)


async def get_index_by_text_task(user_response: str, language: str) -> int | None:
    """
    Берет на вход строку с заданием и выдает индекс задания в словаре

    Параметры:
    - user_response (str): Ответ юзера в виде строки задания
    - language (str): Язык пользователя

    Возвращает:
    - int: Индекс задания в словаре
    """
    try:
        print("def get_index_of_num")
        if language == "RU":
            index = user_response[9:]
        elif language == "ENG":
            index = user_response[6:]
        else:
            return None
        print("get_index_by_text_task ==== " + index)
        return int(index) - 1
    except Exception as e:
        return None


async def send_task_info(message: types.Message, task_index: int):
    """
    Отправляет информацию о задании пользователю.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - task_index (int): Индекс задания.

    Возвращает:
    - None
    """
    language = await get_language_for_user(message.from_user.id)
    tasks_list = list(tasks.values())
    if task_index >= 0 and task_index < len(tasks_list):
        task = tasks_list[task_index]
        reply = await get_message(other_messages, "NOT_DESC_TEXT", language)
        description = task["description"].get(language, reply)
        points = task["points"]
        image_path = task.get("image", "")
        # Format message text
        message_text = await get_message(other_messages, "TASK_TEXT", language, description=description, points=points)

        # Send image (if specified) and message text
        if image_path:
            await message.answer_photo(photo=types.FSInputFile(path="tasks/" + image_path), caption=message_text,
                                       parse_mode="MARKDOWN")
        else:
            await message.answer(text=message_text, parse_mode="MARKDOWN")
    else:
        reply = await get_message(other_messages, "TASK_NOT_FOUND_TEXT", language)
        await message.answer(text=reply, parse_mode="MARKDOWN")


async def send_all_tasks_info(message: types.Message, tasks_done):
    """
    Отправляет информацию обо всех заданиях пользователю.

    Параметры:
    - message (types.Message): Сообщение от пользователя.

    Возвращает:
    - None
    """
    language = await get_language_for_user(message.from_user.id)
    # user = await get_user_details(message.from_user.id)
    # tasks_done = user.get("TASKS_DONE", [])
    tasks_list = [task for index, task in enumerate(tasks.values()) if index not in tasks_done]
    all_tasks_info = []

    for task_index, task in enumerate(tasks_list):
        description = task["description"].get(language, await get_message(other_messages, "NOT_DESC_TEXT", language))
        points = task["points"]
        task_info = await get_message(other_messages, "TASK_TEXT", language, description=description, points=points)
        all_tasks_info.append(f"Task #{task_index + 1}:{task_info}")

    if not all_tasks_info:
        reply = await get_message(other_messages, "NO_TASKS_TEXT", language)
        await message.answer(text=reply, parse_mode="MARKDOWN")
    else:
        all_tasks_message = "\n".join(all_tasks_info)
        await message.answer(text=all_tasks_message, parse_mode="MARKDOWN")


async def get_puzzle_from_task(index_task: int) -> str:
    """
    Возвращает название защиты задания.

    Параметры:
    - index_task (int): Индекс задания.

    Возвращает:
    - str: название защиты задания
    """
    # index_task -= 1
    print("def get_protection_from_task")
    value_at_index = list(tasks.values())[index_task]
    print(value_at_index)
    return value_at_index["puzzle"]
