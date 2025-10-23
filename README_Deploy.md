#  Rental Backend — Production Deployment Guide

Полностью контейнеризированный бэкенд на **Django + DRF + MySQL + Nginx + Gunicorn**.  
Проект разворачивается одной командой через **Docker Compose**.

 Описание
Бэкенд-сервис для платформы аренды жилья.  
Реализованы функции:
- управление пользователями (арендодатель, арендатор);
- создание и бронирование объявлений;
- система отзывов и рейтингов;
- автоматическая рассылка уведомлений (email);
- логирование действий в `src/logs/app.log`.

---

##  Стек технологий
- **Python 3.12**
- **Django 5 + DRF**
- **MySQL 8.4**
- **Celery + Redis** — для фоновых задач (email)
- **Docker + docker-compose**


#  Структура проекта
rental-backend/
│
├── docker-compose.yml # dev-режим (runserver)
├── docker-compose.prod.yml # prod-режим (gunicorn + nginx)
├── Dockerfile
├── start_prod.sh # скрипт запуска в prod
├── nginx/
│ └── default.conf # конфигурация nginx
├── src/
│ ├── config/ # настройки Django
│ ├── users/ listings/ bookings/ reviews/
│ └── static/ # сюда collectstatic собирает файлы
│
└── .env.prod # переменные окружения для prod


src/
├── bookings/        # бронирования + сигналы
├── listings/        # объявления
├── reviews/         # отзывы
├── users/           # пользователи
├── locations/       # географические модели
├── config/          # настройки Django
├── logs/            # лог-файлы
└── management/      # команды seed_all, seed_locations

 Тестирование

Проект покрыт тестами на уровне основных модулей — аутентификация, объявления, бронирования и отзывы.
Тесты написаны с использованием pytest и pytest-django.
Для их выполнения используется тестовая база данных, создаваемая автоматически при запуске.

 Запуск тестов
pytest -v


или для проверки конкретного модуля:

pytest tests/test_bookings.py -v

 Структура тестов

tests/test_auth.py	Проверяет регистрацию, вход пользователя и выдачу JWT-токенов. Тестирует корректность валидации email, пароля и ролей (Tenant/Host).

tests/test_listings.py	  Проверяет CRUD-операции над объявлениями (создание, редактирование, удаление, фильтрация и сортировка). Убедиться, что только владелец может редактировать или удалять объект.

tests/test_bookings.py	 Проверяет создание бронирований, работу проверки пересечений дат, а также сценарии подтверждения, отклонения и отмены бронирования. Включает тест сигналов при изменении статуса брони и soft delete.

tests/test_reviews.py	 Проверяет добавление отзывов и пересчёт рейтинга объявления. Проверяет, что отзыв можно оставить только по завершённому бронированию и один раз для конкретного пользователя.

 Примеры сценариев

- Авторизация

Регистрация нового пользователя.

Попытка входа с неверным паролем.

Получение JWT-токена и доступ к защищённым эндпоинтам.

- Объявления

Создание нового объявления арендодателем.

Попытка редактирования объявления другим пользователем (ожидается 403).

Поиск и фильтрация по цене и городу.

Проверка сортировки по дате и цене.

- Бронирование

Создание брони с валидными датами.

Попытка создать пересекающуюся бронь (ожидается ошибка).

Подтверждение брони арендодателем.

Отмена брони арендатором.

Проверка, что при подтверждении одной брони остальные отклоняются (сигналы работают).

- Отзывы

Добавление отзыва после завершения бронирования.

Попытка повторного отзыва от того же пользователя (ожидается ошибка).

Проверка автоматического обновления рейтинга объявления.

- Используемые фикстуры

db — создаёт тестовую базу данных.

client — REST API клиент для тестирования эндпоинтов.

user_host, user_tenant — тестовые пользователи разных ролей.

listing_factory, booking_factory — генерация тестовых данных.
---

##  1. Подготовка окружения

```bash
# Django
DEBUG=0
SECRET_KEY=your-super-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# MySQL
MYSQL_DATABASE=rental
MYSQL_USER=rental
MYSQL_PASSWORD=rental
MYSQL_ROOT_PASSWORD=root

# Django DB Settings
DB_ENGINE=django.db.backends.mysql
DB_NAME=rental
DB_USER=rental
DB_PASSWORD=rental
DB_HOST=db
DB_PORT=3306


 2. Production Docker Compose

Файл: docker-compose.prod.yml

version: "3.9"

services:
  db:
    image: mysql:8.4
    restart: always
    environment:
      MYSQL_DATABASE: rental
      MYSQL_USER: rental
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:-rental}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-root}
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    command: sh /app/start_prod.sh
    environment:
      DB_HOST: db
      DB_PORT: "3306"

      DEBUG: "0"
      SECRET_KEY: ${SECRET_KEY:-change-me}
      ALLOWED_HOSTS: ${ALLOWED_HOSTS:-localhost,127.0.0.1}
      DJANGO_SETTINGS_MODULE: src.config.settings
      PYTHONPATH: /app

      DB_ENGINE: django.db.backends.mysql
      DB_NAME: rental
      DB_USER: rental
      DB_PASSWORD: ${MYSQL_PASSWORD:-rental}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - static_data:/app/src/static
    expose:
      - "8000"
    restart: always

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
      - static_data:/app/src/static
    depends_on:
      - api
    restart: always

volumes:
  db_data:
  static_data:

 3. Сборка и запуск (первый раз)

docker compose -f docker-compose.prod.yml down -v
docker compose -f docker-compose.prod.yml up --build

 При запуске:

MySQL создаст базу rental

Django выполнит миграции

Соберёт статику → /app/src/static

Gunicorn поднимет сервер на 0.0.0.0:8000

Nginx отдаст приложение по http://localhost

 4. Проверка

API: http://localhost/api/

Swagger Docs: http://localhost/api/docs/

Django Admin: http://localhost/admin/



  5. Управление контейнерами
Команда	Описание
docker compose -f docker-compose.prod.yml up -d	Запустить в фоне
docker compose -f docker-compose.prod.yml down	Остановить
docker compose -f docker-compose.prod.yml down -v	Полностью очистить (вместе с БД)
docker compose -f docker-compose.prod.yml logs -f api	Смотреть логи Django
docker compose -f docker-compose.prod.yml exec api bash	Войти внутрь контейнера Django

   6. Проверка статики вручную
docker compose -f docker-compose.prod.yml exec api ls /app/src/static/admin/css
docker compose -f docker-compose.prod.yml exec nginx ls /app/src/static/admin/css

   7. (Опционально) HTTPS

Для деплоя на сервер добавь:

Nginx + Certbot для SSL (порт 443)

Настрой server_name в nginx/default.conf

Открой порты 80 и 443 на сервере

  8. Резервное копирование БД

docker compose -f docker-compose.prod.yml exec db mysqldump -u root -p rental > ba