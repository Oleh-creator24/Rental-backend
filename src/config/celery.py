from __future__ import absolute_import, unicode_literals
import os
import logging
from celery import Celery
from celery.signals import setup_logging

# Указываем Django-настройки по умолчанию
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Инициализируем приложение Celery
app = Celery("config")

# Загружаем конфигурацию Celery из Django settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находит все файлы tasks.py в приложениях Django
app.autodiscover_tasks()

# ---------- Настройки по умолчанию ----------
# Можно использовать Redis или RabbitMQ — достаточно заменить broker_url
app.conf.update(
    broker_url="redis://localhost:6379/0",  # или amqp://guest:guest@localhost//
    result_backend="redis://localhost:6379/0",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Berlin",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

# ---------- Настройка логирования ----------
@setup_logging.connect
def config_loggers(*args, **kwargs):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] — %(message)s",
    )

# ---------- Тестовая задача ----------
@app.task(bind=True)
def debug_task(self):
    print(f"Celery работает! Request: {self.request!r}")
