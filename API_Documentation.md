#  Rental Backend API — Документация (v1.0.0)

**Описание:**  
REST API сервиса аренды жилья с авторизацией JWT, CRUD для объявлений, бронированиями, отзывами и модулем аналитики (просмотры и поисковые запросы).  
Все временные метки сохраняются в формате UTC, а цены — в валюте владельца объявления с возможностью фильтрации и отображения по выбранной валюте пользователя.

---

##  Авторизация и пользователи

| Эндпоинт | Метод | Описание |
|-----------|--------|----------|
| `/api/v1/token/` | POST | Получение пары JWT токенов (access + refresh) |
| `/api/v1/token/refresh/` | POST | Обновление access токена |
| `/api/v1/users/register/` | POST | Регистрация нового пользователя (роль: TENANT / LANDLORD) |
| `/api/v1/users/me/` | GET | Получение данных текущего авторизованного пользователя |

---

##  Объявления (Listings)

| Эндпоинт | Метод | Описание |
|-----------|--------|----------|
| `/api/v1/listings/` | GET | Получение списка объявлений с фильтрацией и пагинацией |
| `/api/v1/listings/` | POST | Создание нового объявления (только LANDLORD) |
| `/api/v1/listings/{id}/` | GET | Просмотр конкретного объявления |
| `/api/v1/listings/{id}/` | PUT / PATCH | Редактирование объявления |
| `/api/v1/listings/{id}/` | DELETE | Удаление объявления |
| `/api/v1/listings/search-trends/` | GET | Популярные поисковые запросы (тренды) |

**Поля модели:**
- `title` — Заголовок объявления  
- `description` — Описание  
- `price` — Цена  
- `price_currency` — Валюта (`EUR`, `USD`, `GBP`, `CHF`, `PLN`, `CZK`)  
- `is_available` — Доступно ли жильё  
- `country` — Страна  
- `city` — Город  
- `street` — Улица  
- `house_number` — Номер дома  
- `apartment_number` — Номер квартиры (опционально)  
- `view_count` — Количество просмотров  
- `created_at` — Дата создания (UTC)  
- `owner` — Владелец (арендодатель)

**Параметры запроса (фильтры):**
- `search` — поиск по названию, описанию, городу и стране  
- `country` — фильтр по стране  
- `currency` — фильтр по валюте (`?currency=EUR`)  
- `is_available` — фильтр по доступности (`true/false`)  
- `ordering` — сортировка (`price`, `created_at`, `view_count`)  

---

##  Отзывы (Reviews)

| Эндпоинт | Метод | Описание |
|-----------|--------|----------|
| `/api/v1/listings/{listing_pk}/reviews/` | GET | Список отзывов по объявлению |
| `/api/v1/listings/{listing_pk}/reviews/` | POST | Добавление нового отзыва |
| `/api/v1/listings/{listing_pk}/reviews/{id}/` | GET | Просмотр конкретного отзыва |
| `/api/v1/listings/{listing_pk}/reviews/{id}/` | PUT / PATCH | Редактирование отзыва |
| `/api/v1/listings/{listing_pk}/reviews/{id}/` | DELETE | Удаление отзыва |

**Поля модели:**
- `rating` — Оценка (1–5)  
- `comment` — Текст отзыва  
- `user` — Автор отзыва  
- `listing` — Ссылка на объявление  

---

##  Бронирования (Bookings)

| Эндпоинт | Метод | Описание |
|-----------|--------|----------|
| `/api/v1/bookings/` | GET | Список всех бронирований пользователя |
| `/api/v1/bookings/` | POST | Создание бронирования |
| `/api/v1/bookings/{id}/` | GET | Просмотр информации о бронировании |
| `/api/v1/bookings/{id}/` | PUT / PATCH | Изменение дат бронирования |
| `/api/v1/bookings/{id}/` | DELETE | Удаление бронирования |
| `/api/v1/bookings/{id}/approve/` | POST | Подтверждение бронирования (владелец) |
| `/api/v1/bookings/{id}/reject/` | POST | Отклонение бронирования |
| `/api/v1/bookings/{id}/cancel/` | POST | Отмена бронирования пользователем |

**Поля модели:**
- `listing` — Объявление  
- `user` — Кто забронировал  
- `start_date`, `end_date` — Даты аренды  
- `status` — `pending`, `approved`, `rejected`, `cancelled`  

---

##  Аналитика (Stats)

| Эндпоинт | Метод | Описание |
|-----------|--------|----------|
| `/api/v1/stats/top_listings/` | GET | Топ-10 популярных объявлений |
| `/api/v1/stats/top_queries/` | GET | Топ-10 поисковых запросов |
| `/api/v1/stats/add_view/` | POST | Запись просмотра объявления |
| `/api/v1/stats/add_query/` | POST | Запись поискового запроса |
| `/api/v1/stats/summary/` | GET | Общая статистика и активность за последние 7 дней |

**Поля статистики summary:**
- `total_views` — Общее количество просмотров  
- `unique_users` — Количество уникальных пользователей  
- `total_queries` — Количество поисковых запросов  
- `top_listings` — Топ-3 популярных объявления  
- `activity_last_7_days` — Активность по дням: просмотры и запросы  

---

##  Время и часовые пояса

- Все временные значения (`created_at`, `updated_at`) хранятся в формате **UTC**  
- Django автоматически сохраняет временные метки как *осознанные (aware)*  
- В будущем возможно добавление параметра `?tz=Europe/Berlin` для локального отображения времени пользователю

---

##  Валюты

- Поддерживаемые валюты: `EUR`, `USD`, `GBP`, `CHF`, `PLN`, `CZK`  
- В базе хранится `price` в валюте владельца (`price_currency`)  
- Пользователь может указать желаемую валюту отображения (`?currency=USD`)  
- Конвертация выполняется через API или фиксированные коэффициенты  

---

##  Документация API

| Тип | URL |
|------|-----|
| Swagger UI | [http://127.0.0.1:8000/api/v1/schema/swagger-ui/](http://127.0.0.1:8000/api/v1/schema/swagger-ui/) |
| Redoc | [http://127.0.0.1:8000/api/v1/schema/redoc/](http://127.0.0.1:8000/api/v1/schema/redoc/) |
| OpenAPI JSON Schema | [http://127.0.0.1:8000/api/v1/schema/](http://127.0.0.1:8000/api/v1/schema/) |

---

##  Используемые технологии

- **Django + Django REST Framework (DRF)** — API и маршрутизация  
- **MySQL** — основная база данных  
- **JWT (SimpleJWT)** — аутентификация пользователей  
- **drf-spectacular** — автогенерация документации (OpenAPI / Swagger / Redoc)  
- **Docker Compose** — контейнеризация приложения  
- **Gunicorn + Nginx** — продакшн сервер  
- **AWS EC2 / S3** — планируемое размещение и хранение медиафайлов  

---

##  Пример структуры проекта

src/
├── bookings/
├── listings/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ └── filters.py
├── reviews/
├── stats/
├── users/
├── config/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
└── manage.py