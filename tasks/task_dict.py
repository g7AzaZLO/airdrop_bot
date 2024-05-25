# Словарь задач
tasks = {}


async def update_tasks(new_tasks):
    global tasks
    tasks.update(new_tasks)
    print(tasks)


protection_for_admins = ["screen_check", "twitter_screen_check"]
