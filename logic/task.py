from aiogram import types, Router
from tasks.task_dict import tasks

task_router = Router()


async def get_all_points() -> int:
    print("def get_all_points")
    point_counter = 0
    for task in tasks:
        point_counter += tasks[task]["points"]
    return point_counter


async def get_protection_from_task(index_task: int) -> str:
    index_task -= 1
    print("def get_protection_from_task")
    value_at_index = list(tasks.values())[index_task]
    print(value_at_index)
    return value_at_index["protection"]


async def get_num_of_tasks() -> int:
    print("def get_num_of_tasks")
    return len(tasks)


async def get_index_of_num(user_response: str, language: str) -> int | None:
    print("def get_index_of_num")
    if language == "RU":
        index = user_response[9:]
    elif language == "ENG":
        index = user_response[6:]
    else:
        return None
    return int(index)


async def return_task_info(message: types.Message, task: str) -> None:
    print("def return_task_info")
    info = tasks[task]
    photo = info["image"]
    description = info["description"]
    points = info["points"]
    await message.answer_photo(photo)
    await message.answer(text=description)
