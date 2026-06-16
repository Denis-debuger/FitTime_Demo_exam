# FitTime Demo Exam

Простое Django-приложение для онлайн-записи в фитнес-клуб.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

После миграций создаются демо-тренировки. Администратор создаётся автоматически при открытии главной страницы или страницы входа.

## Доступ администратора

- Логин: `Admin`
- Пароль: `FitTimeAdmin`

## Страницы

- `/` — главная страница с каруселью.
- `/register/` — регистрация клиента.
- `/login/` — авторизация.
- `/trainings/` — список тренировок.
- `/booking/` — оформление записи.
- `/cabinet/` — личный кабинет клиента.
- `/panel/` — панель администратора.
