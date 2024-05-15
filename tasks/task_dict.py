# Словарь задач
# TODO придумать как интегрировать язык в description
# TODO надо переносить этот лсовать в отдельную таблицу БД, чтобы можно было добавлять задания не перезапуская бота
tasks = {
    "task1": {
        "image": "task1.png",
        "description": {
            "RU": "Подпишитесь на наш канал Telegram",
            "ENG": "Subscribe to our Telegram channel"
        },
        "points": 50,
        "type": "telegram_sub",
        "protection": None
    },
    "task2": {
        "image": "",
        "description": {
            "RU": "Сделайте репост нашего поста в Twitter",
            "ENG": "Retweet our post on Twitter"
        },
        "points": 100,
        "type": "twitter_retweet",
        "protection": "bot_check"
    },
    "task3": {
        "image": "",
        "description": {
            "RU": "Оставьте комментарий в Twitter",
            "ENG": "Leave a comment on Twitter"
        },
        "points": 150,
        "type": "twitter_comment",
        "protection": "screen_check"
    },
    "task4": {
        "image": "",
        "description": {
            "RU": "Оставьте комментарий в Telegram",
            "ENG": "Leave a comment on Telegram"
        },
        "points": 200,
        "type": "telegram_comment",
        "protection": "screen_check"
    }
}

protection_fot_admins = ["screen_check",]