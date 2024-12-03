# Используйте подходящий Python-образ
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установим зависимости
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем исходный код проекта
COPY . /app/

# Собираем статику
RUN python manage.py collectstatic --noinput

# Установка gunicorn
RUN pip install gunicorn

# Убедимся, что у нас установлен Celery
RUN pip install celery

# Установка Flower
RUN pip install flower

# Зададим команду по умолчанию
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "djangoProject_all.wsgi:application", "--workers 3"]