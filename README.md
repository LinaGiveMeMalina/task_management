# Task Management API

**REST API** для управления задачами

## Стек
- Python 3.12
- FastAPI
- SQLAlchemy 2.0 (async) + asyncpg
- Alembic (миграции)
- PostgreSQL
- Poetry
- pytest + pytest-asyncio + httpx
- Docker / Docker Compose

## Быстрый старт

### - Создание файла `.env` с переменными окружения из `.env.template`

```bash
cp .env.template .env
```

### - Запуск в Docker

```bash
make up
```
**API** будет доступен на http://localhost:8000

Документация **Swagger**: http://localhost:8000/docs

### - Установка зависимостей (через poetry):

```bash
make dev.install
```

## Работа с миграциями

### Накатить миграции в базу:

```bash
make db.migrate
```

### Откатить последнюю миграцию:

```bash
make db.migrate.down
```

## Тесты

### Запустить тесты:

```bash
make test
```

## API (кратко)

**POST /tasks/** — создать задачу

**GET /tasks/** — список задач

**GET /tasks/{task_id}** — получить по id

**PATCH /tasks/{task_id}** — обновить

**DELETE /tasks/{task_id}** — удалить (мягкое удаление)
