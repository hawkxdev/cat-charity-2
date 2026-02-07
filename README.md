# QRKot - Благотворительный фонд поддержки котиков

REST API для автоматического распределения пожертвований по целевым проектам.

## Описание

Приложение позволяет:
- Создавать целевые проекты со сбором конкретных сумм
- Принимать пожертвования от пользователей
- Автоматически распределять пожертвования по проектам (FIFO)
- Регистрировать и авторизовать пользователей (JWT)
- Разграничивать права доступа (user/superuser)

## Технологии

- [Python 3.9+](https://www.python.org/)
- [FastAPI 0.111.0](https://fastapi.tiangolo.com/)
- [FastAPI Users 13.0.0](https://fastapi-users.github.io/fastapi-users/)
- [SQLAlchemy 2.0.29](https://www.sqlalchemy.org/) (async)
- [Pydantic 2.7.1](https://docs.pydantic.dev/)
- [Alembic 1.7.7](https://alembic.sqlalchemy.org/)
- [SQLite](https://www.sqlite.org/) + [aiosqlite](https://aiosqlite.omnilib.dev/)

## Установка

```bash
# Клонировать репозиторий
git clone <url>
cd cat-charity-2

# Создать виртуальное окружение и установить зависимости
uv venv
uv sync --all-extras

# Применить миграции
uv run alembic upgrade head
```

## Запуск

```bash
# Запуск сервера
uv run uvicorn app.main:app --reload

# Документация доступна по адресу
# http://localhost:8000/docs
```

## Разработка

```bash
# Запуск тестов
uv run pytest

# Линтинг
uv run ruff check app/
uv run mypy app/
```

## Структура проекта

```
app/
├── api/endpoints/    # Роутеры (charity_project, donation, user)
├── api/validators.py # Валидаторы бизнес-правил
├── core/             # Конфигурация, БД, FastAPI Users
├── crud/             # CRUD операции (CRUDBase + специфичные)
├── models/           # ORM модели (CharityProject, Donation, User)
├── schemas/          # Pydantic схемы (Create/Update/DB)
├── services/         # Бизнес-логика (investment.py)
└── main.py           # FastAPI instance
```

## API Endpoints

Документация доступна в Swagger UI: `/docs`

### Аутентификация
- `POST /auth/jwt/login` - получить JWT токен
- `POST /auth/jwt/logout` - выйти из системы
- `POST /auth/register` - регистрация пользователя

### Пользователи
- `GET /users/me` - текущий пользователь
- `PATCH /users/me` - редактировать профиль

### Проекты
- `GET /charity_project/` - список всех проектов
- `POST /charity_project/` - создать проект (superuser)
- `PATCH /charity_project/{id}` - редактировать проект (superuser)
- `DELETE /charity_project/{id}` - удалить проект (superuser)

### Пожертвования
- `GET /donation/` - все пожертвования (superuser)
- `GET /donation/my` - мои пожертвования (auth)
- `POST /donation/` - создать пожертвование (auth)

## Автор

Sergey Sokolkin [GitHub](https://github.com/hawkxdev)

Учебный проект курса [Яндекс Практикум](https://practicum.yandex.ru/) (Python-разработчик)
