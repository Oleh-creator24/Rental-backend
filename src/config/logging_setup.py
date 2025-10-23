import os
import logging
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Создаём папку logs, если её нет
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

# Настраиваем формат вывода
LOG_FORMAT = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] — %(message)s"

# Основной логгер
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# === HANDLERS ===

# 1️ — Консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# 2️ — Файл с ротацией (до 5 файлов по 5 MB)
file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Добавляем обработчики к логгеру
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# Отдельные логгеры для модулей (если нужно фильтровать)
logging.getLogger("django").setLevel(logging.WARNING)
logging.getLogger("django.request").setLevel(logging.ERROR)
logging.getLogger("users").setLevel(logging.INFO)
logging.getLogger("bookings").setLevel(logging.INFO)
logging.getLogger("reviews").setLevel(logging.INFO)
logging.getLogger("listings").setLevel(logging.INFO)
logging.getLogger("locations").setLevel(logging.INFO)

logging.info(" Logging system initialized — logs writing to %s", LOG_FILE_PATH)
