import os

from celery import Celery

# Установим переменную окружения Django для Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject_all.settings")

app = Celery("djangoProject_all")

# Загружаем настройки из Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическое обнаружение задач в установленных приложениях Django
app.autodiscover_tasks()
