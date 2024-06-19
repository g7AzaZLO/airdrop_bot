import logging
from colorlog import ColoredFormatter

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание обработчика для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
# Создание цветного форматтера для консоли
color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'white',
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
    },
    secondary_log_colors={},
    style='%'
)

# Создание обработчика для записи логов в файл (только ошибки)
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)

# Создание форматтера и добавление его в обработчики
file_formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')

# Добавление цветного форматтера в консольный обработчик
console_handler.setFormatter(color_formatter)
# Добавление обычного форматтера в файловый обработчик
file_handler.setFormatter(file_formatter)

# Добавление обработчиков в логгер
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger():
    return logger
