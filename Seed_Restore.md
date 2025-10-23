**Seed \& Restore Database**



 **1. Генерация тестовых данных**



**Команда `seed\_all` создаёт реалистичные данные для тестирования:**



**```bash**

**python src/manage.py seed\_all**





**Что создаётся:**



**80 арендодателей (host\_1...host\_80)**



**50 арендаторов (tenant\_1...tenant\_50)**



**10 гостей (guest\_1...guest\_10)**



**20 городов (через Faker)**



**200 объявлений**



**150 бронирований (без пересечений)**



**50 отзывов**



**Все пароли по умолчанию — 1234.**



**2. Сохранение дампа базы данных**



**Чтобы не пересоздавать данные заново:**



**python src/manage.py dumpdata --natural-primary --natural-foreign --indent 2 --output src/backup\_data.json**





**Файл сохранится как src/backup\_data.json.**



**3. Восстановление данных из резервной копии**

**python src/manage.py loaddata src/backup\_data.json**





**Если возникает ошибка кодировки Windows (charmap codec),**

**используйте PowerShell с UTF-8:**



**chcp 65001**

**python src/manage.py loaddata src/backup\_data.json**



**4. Очистка перед пересозданием**



**Перед повторной генерацией рекомендуется очистить таблицы:**



**python src/manage.py flush**



**5. Проверка корректности данных**



**После загрузки убедитесь, что данные есть в БД:**



**python src/manage.py shell**

**>>> from listings.models import Listing**

**>>> Listing.objects.count()**

**200**



**6. Админ-панель**



**Логин: admin@example.com**

**Пароль: 1234**



**Админка доступна по адресу:**

**http://127.0.0.1:8000/admin/**

