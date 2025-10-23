#!/usr/bin/env sh
set -e

echo " Wait DB on $DB_HOST:$DB_PORT ..."
# Универсальная проверка TCP-порта (nc уже есть в образе)
for i in $(seq 1 60); do
  nc -z "$DB_HOST" "$DB_PORT" && break
  echo "  ...still waiting ($i)"
  sleep 1
done

echo " DB is up. Running migrations..."
python manage.py migrate --noinput

echo " Collect static..."
python manage.py collectstatic --noinput

echo " Starting gunicorn..."
exec gunicorn src.config.wsgi:application --bind 0.0.0.0:8000 --workers 3
