# Словарь задач
# TODO придумать как интегрировать язык в description
tasks = {
    "task1": {
        "image": "task1.png",
        "description": "Подпишитесь на наш канал Telegram",
        "points": 50,
        "type": "telegram_sub"
    },
    "task2": {
        "image": "task2.png",
        "description": "Сделайте репост нашего поста в Twitter",
        "points": 100,
        "type": "twitter_retweet"
    },
    "task3": {
        "image": "task3.png",
        "description": "Оставьте комментарий в Twitter",
        "points": 150,
        "type": "twitter_comment"
    },
    "task4": {
        "image": "task4.png",
        "description": "Оставьте комментарий в Telegram",
        "points": 200,
        "type": "telegram_comment"
    }
}

# Словарь типов задач
task_types = {
    "telegram_sub": {
        "protection": "bot_check"
    },
    "twitter_retweet": {
        "protection": None
    },
    "twitter_comment": {
        "protection": "screen_check"
    }
}