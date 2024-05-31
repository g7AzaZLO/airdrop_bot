# Словарь задач
from DB.database_logic import get_all_tasks

tasks = {}


async def update_tasks(new_tasks):
    global tasks
    tasks.clear()  # Удаляем все существующие задачи
    tasks.update(new_tasks)  # Обновляем новыми задачами
    print(tasks)


async def change_tasks():
    new_tasks = await get_all_tasks()
    print("Tasks have been updated.")
    await update_tasks(new_tasks)


protection_for_admins = ["screen_check", "twitter_screen_check"]
