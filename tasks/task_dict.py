# Словарь задач
tasks = {5: {
    '_id': 5,
    'description': {
        "ENG": """
🔹 *Follow our Twitter page*:
[https://twitter.com/buyordie_ton]
        """,
        "RU": """
🔹 *Подпишитесь на наш Twitter*:
[https://twitter.com/buyordie_ton]
        """
    },
    'image': '',
    'points': 100,
    'protection': 'twitter_screen_check',
    'type': 'twitter_sub'
}}


async def update_tasks(new_tasks):
    global tasks
    tasks.update(new_tasks)
    print(tasks)


protection_fot_admins = ["screen_check", "twitter_screen_check"]
