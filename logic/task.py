import logging
from aiogram import types, Router
from DB.database_logic import get_language_for_user, get_user_details
from tasks.task_dict import tasks
from handlers.standart_handler import get_message
from messages.other_messages import other_messages
from settings.logging_config import get_logger

logger = get_logger()

task_router = Router()


async def get_all_points() -> int:
    """
    Возвращает общее количество очков за все существующие задания.

    Возвращает:
    - int: Общее количество очков за все существующие задания.
    """
    logger.info("Executing get_all_points")
    point_counter = 0
    for task in tasks:
        point_counter += tasks[task]["points"]
    logger.info(f"Total points for all tasks: {point_counter}")
    return point_counter


async def get_protection_from_task(index_task: int) -> str:
    """
    Возвращает название защиты задания.

    Параметры:
    - index_task (int): Индекс задания.

    Возвращает:
    - str: название защиты задания
    """
    logger.info("Executing get_protection_from_task")
    value_at_index = list(tasks.values())[index_task]
    logger.info(f"Protection for task {index_task}: {value_at_index}")
    return value_at_index["protection"]


async def get_points_from_task(index_task: int) -> int:
    """
    Возвращает количество поинтов за задание.

    Параметры:
    - index_task (int): Индекс задания.

    Возвращает:
    - int: количество поинтов за задание
    """
    logger.info("Executing get_points_from_task")
    value_at_index = list(tasks.values())[index_task]
    logger.info(f"Points for task {index_task}: {value_at_index}")
    return value_at_index["points"]


async def calculate_total_points(done_tasks: list) -> int:
    """
    Вычисляет общее количество очков за выполненные задания.

    Параметры:
    - done_tasks (list): Список индексов выполненных заданий.

    Возвращает:
    - int: Общее количество очков за все выполненные задания.
    """
    logger.info("Executing calculate_total_points")
    total_points = 0
    for index in done_tasks:
        value_at_index = list(tasks.values())[index]
        if value_at_index:
            total_points += value_at_index["points"]
    logger.info(f"Total points for completed tasks: {total_points}")
    return total_points


async def get_num_of_tasks() -> int:
    """
    Возвращает количество существующих заданий.

    Возвращает:
    - int: Количество существующих заданий.
    """
    logger.info("Executing get_num_of_tasks")
    num_tasks = len(tasks)
    logger.info(f"Number of tasks: {num_tasks}")
    return num_tasks


async def get_index_by_text_task(task_text: str, language: str) -> int | None:
    """
    Получает индекс задачи по тексту задачи.

    Параметры:
    - task_text (str): Текст задачи.
    - language (str): Язык ("RU" или "ENG").

    Возвращает:
    - int: Индекс задачи.
    """
    logger.debug("def get_index_by_text_task")
    if task_text.startswith("task_"):
        try:
            index_task = int(task_text.replace("task_", "")) - 1
            logger.debug(f"get_index_by_text_task ==== {index_task}")
            return index_task
        except ValueError as e:
            logger.error(f"An error occurred: {e}")
            return None
    return None


async def send_task_info(callback_query: types.CallbackQuery, task_index: int, reply_markup=None, edit=False):
    """
    Отправляет информацию о задании пользователю.

    Параметры:
    - message (types.Message): Сообщение от пользователя.
    - task_index (int): Индекс задания.
    - reply_markup (Optional): Клавиатура для отправки вместе с сообщением.
    - edit (bool): Указывает, нужно ли редактировать существующее сообщение.

    Возвращает:
    - None
    """
    try:
        language = await get_language_for_user(callback_query.from_user.id)
        tasks_list = list(tasks.values())
        if 0 <= task_index < len(tasks_list):
            task = tasks_list[task_index]
            no_desc = await get_message(other_messages, "NOT_DESC_TEXT", language)
            description = task["description"].get(language, no_desc)
            points = task["points"]
            photo_path = task.get("image", "")
            reply = await get_message(other_messages, "TASK_TEXT", language, description=description,
                                             points=points)
            if photo_path:
                if callback_query.message.photo:
                    await callback_query.message.edit_media(
                        media=types.InputMediaPhoto(media=photo_path)
                    )
                    await callback_query.message.edit_caption(inline_message_id=str(callback_query.message.message_id),
                                                              parse_mode="MARKDOWN", caption=reply,
                                                              reply_markup=reply_markup)
                else:
                    await callback_query.message.delete()
                    await callback_query.message.answer_photo(
                        photo=photo_path, caption=reply, reply_markup=reply_markup,
                        parse_mode="MARKDOWN"
                    )
            else:
                if callback_query.message.text:
                    await callback_query.message.edit_text(text=reply, reply_markup=reply_markup,
                                                           parse_mode="MARKDOWN")
                else:
                    await callback_query.message.delete()
                    await callback_query.message.answer(text=reply, reply_markup=reply_markup,
                                                        parse_mode="MARKDOWN")
        else:
            reply = await get_message(other_messages, "TASK_NOT_FOUND_TEXT", language)
            if callback_query.message.text:
                await callback_query.message.edit_text(text=reply, reply_markup=reply_markup,
                                        parse_mode="MARKDOWN")
            else:
                await callback_query.message.delete()
                await callback_query.message.answer(text=reply, reply_markup=reply_markup,
                                     parse_mode="MARKDOWN")
    except Exception as e:
        logger.error("An error occurred in send_task_info: %s", e)



# async def send_all_tasks_info(message: types.Message, tasks_done):
#     """
#     Отправляет информацию обо всех заданиях пользователю.
#
#     Параметры:
#     - message (types.Message): Сообщение от пользователя.
#
#     Возвращает:
#     - None
#     """
#     try:
#         language = await get_language_for_user(message.from_user.id)
#         tasks_list = [task for index, task in enumerate(tasks.values()) if index not in tasks_done]
#         all_tasks_info = []
#
#         for task_index, task in enumerate(tasks_list):
#             description = task["description"].get(language,
#                                                   await get_message(other_messages, "NOT_DESC_TEXT", language))
#             points = task["points"]
#             task_info = await get_message(other_messages, "TASK_TEXT", language, description=description, points=points)
#             all_tasks_info.append(f"Task #{task_index + 1}:{task_info}")
#
#         if not all_tasks_info:
#             reply = await get_message(other_messages, "NO_TASKS_TEXT", language)
#             await message.answer(text=reply, parse_mode="MARKDOWN")
#         else:
#             all_tasks_message = "\n".join(all_tasks_info)
#             await message.answer(text=all_tasks_message, parse_mode="MARKDOWN")
#     except Exception as e:
#         logger.error("An error occurred in send_all_tasks_info: %s", e)
async def send_all_tasks_info(message: types.Message, language):
    """
    Отправляет информацию обо всех заданиях пользователю.

    Параметры:
    - message (types.Message): Сообщение от пользователя.

    Возвращает:
    - None
    """
    try:
        tasks_list = [task for index, task in enumerate(tasks.values())]
        all_tasks_info = []

        for task_index, task in enumerate(tasks_list):
            description = task["description"].get(language,
                                                  await get_message(other_messages, "NOT_DESC_TEXT", language))
            points = task["points"]
            task_info = await get_message(other_messages, "TASK_TEXT", language, description=description, points=points)
            all_tasks_info.append(f"Task #{task_index + 1}:{task_info}")

        if not all_tasks_info:
            reply = await get_message(other_messages, "NO_TASKS_TEXT", language)
            return reply
        else:
            all_tasks_message = "\n".join(all_tasks_info)
            return all_tasks_message
    except Exception as e:
        logger.error("An error occurred in send_all_tasks_info: %s", e)


async def get_puzzle_from_task(index_task: int) -> str:
    """
    Возвращает название защиты задания.

    Параметры:
    - index_task (int): Индекс задания.

    Возвращает:
    - str: название защиты задания
    """
    try:
        logger.debug("def get_protection_from_task")
        value_at_index = list(tasks.values())[index_task]
        logger.debug(value_at_index)
        return value_at_index["puzzle"]
    except Exception as e:
        logger.error("An error occurred in get_puzzle_from_task: %s", e)
        return ""
