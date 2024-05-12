# Словарь задач
# TODO придумать как интегрировать язык в description
tasks = {
    "task1": {
        "image": "task1.png",
        "description": "Подпишитесь на наш канал Telegram",
        "points": 50,
        "type": "telegram_sub",
        "protection": None
    },
    "task2": {
        "image": "task2.png",
        "description": "Сделайте репост нашего поста в Twitter",
        "points": 100,
        "type": "twitter_retweet",
        "protection": "bot_check"
    },
    "task3": {
        "image": "task3.png",
        "description": "Оставьте комментарий в Twitter",
        "points": 150,
        "type": "twitter_comment",
        "protection": "screen_check"
    },
    "task4": {
        "image": "task4.png",
        "description": "Оставьте комментарий в Telegram",
        "points": 200,
        "type": "telegram_comment",
        "protection": "screen_check"
    }
}

protection_fot_admins = ["screen_check",]