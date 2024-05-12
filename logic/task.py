from aiogram import types, Router
from tasks.task_dict import tasks, task_types

task_router = Router()


async def get_all_points() -> int:
    print("def get_all_points")
    point_counter = 0
    for task in tasks:
        point_counter += tasks[task]["points"]
    return point_counter


async def get_num_of_tasks() -> int:
    print("def get_num_of_tasks")
    return len(tasks)


async def return_task_info(message: types.Message, task: str) -> None:
    print("def return_task_info")
    info = tasks[task]
    photo = info["image"]
    description = info["description"]
    points = info["points"]
    await message.answer_photo(photo)
    await message.answer(text=description)
