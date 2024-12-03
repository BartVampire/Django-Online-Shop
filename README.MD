# 🛍️ Интернет-магазин одежды на Django

Добро пожаловать в репозиторий проекта **интернет-магазина одежды**!  
Проект создан на основе **Django**, с использованием **Docker Compose**, **Celery**, **Flower** и **nginx**. Включает все необходимые функции для полноценной работы онлайн-магазина:  
управление пользователями, каталог товаров, корзину, заказы и многое другое.  

---

## ✨ Основные возможности

- 🔐 **Аутентификация и управление пользователями**: регистрация, вход, восстановление пароля.  
- 👗 **Каталог товаров**: модели **Product**, **Category**, **Brand**, с вариантами товаров и характеристиками.  
- 🛒 **Корзина и заказы**: управление корзиной, создание и отслеживание заказов.  
- 📦 **Администрирование**: встроенная панель Django Admin.  
- 🌐 **Интерфейс**: продуманные HTML-шаблоны с динамическим контентом (AJAX).  
- 📧 **E-mail уведомления**: настройка отправки писем пользователям.  
- ⚡ **Асинхронные задачи**: обработка фоновых задач с помощью **Celery** и мониторинг через **Flower**.  

---

## 🛠️ Технологии

<div align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white" alt="Celery"/>
  <img src="https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="nginx"/>
</div>


---

## 🚀 Установка и запуск

### 🔧 Установка зависимостей
1. Убедитесь, что у вас установлены:
   - [Docker](https://www.docker.com/)
   - [Docker Compose](https://docs.docker.com/compose/)
2. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/BartVampire/Django-Online-Shop.git

## ⚙️ Настройка окружения
### Создайте файл .env и добавьте следующие переменные:
```bash
- POSTGRES_DB=your_database_name
- POSTGRES_USER=your_database_user
- POSTGRES_PASSWORD=your_database_password
- POSTGRES_HOST=db
- POSTGRES_PORT=5432
- DJANGO_DEBUG=True
- SECRET_KEY=your_secret_key
- EMAIL_HOST_USER=your_email
- EMAIL_HOST_PASSWORD=your_email_password
- REDIS_HOST=redis
- REDIS_PORT=6379
- REDIS_DB=0
- CELERY_BROKER_URL=redis://redis:6379/0
- CELERY_RESULT_BACKEND=redis://redis:6379/0
- FLOWER_USER=flower_user
- FLOWER_PASSWORD=flower_password
```
---
## 🐳 Запуск через Docker Compose

### 1. Соберите и запустите контейнеры:
```
docker compose up --build
```
### 2. Примените миграции базы данных:
````
docker compose exec app python manage.py migrate
````
### 3. Создайте суперпользователя:
````
docker compose exec app python manage.py createsuperuser
````
### Теперь проект доступен по адресу: http://localhost.

---
## 📜 Миграции базы данных

### Чтобы выполнить миграции вручную:
````
docker compose exec app python manage.py makemigrations
docker compose exec app python manage.py migrate
````




