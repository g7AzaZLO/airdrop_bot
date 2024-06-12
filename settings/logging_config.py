import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание обработчика для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Создание обработчика для записи логов в файл (только ошибки)
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)

# Создание форматтера и добавление его в обработчики
formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Добавление обработчиков в логгер
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger():
    return logger
