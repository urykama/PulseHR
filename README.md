# PulseHR — сервис опросов сотрудников

Цифровой сервис для проведения анонимных опросов сотрудников с аналитикой для HR.

## Функционал

- ✅ Создание опросов через админку Django
- ✅ Прохождение опросов сотрудниками (без регистрации)
- ✅ Защита от повторного прохождения
- ✅ Аналитика для HR: графики, средние оценки, тексты ответов
- ✅ Анонимные и именные опросы

## Быстрый старт

```bash
# Склонировать репозиторий
git clone https://github.com/urykama/PulseHR.git
cd PulseHR

# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # или .venv\Scripts\activate на Windows

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver



Технологии
Python 3.10

Django 5.x

SQLite

HTML/CSS
