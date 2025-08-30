# template_project

Готовый шаблон для микросервиса бекенда

- [FastAPI](https://fastapi.tiangolo.com/) - веб-фреймворк
- [uvicorn](https://www.uvicorn.org/) - ASGI сервер
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - миграции
- [PostgreSQL](https://www.postgresql.org/) - реляционная база данных
- [uv](https://docs.astral.sh/uv/) - инструмент для запуска и управления приложениями
- [pytest](https://docs.pytest.org/en/7.4.x/) - тестирование
- [ruff](https://beta.ruff.rs/docs/) - линтер и автоформатер
- [mypy](https://mypy-lang.org/) - статическая типизация
- [pre-commit](https://pre-commit.com/) - хуки для git
- [docker](https://www.docker.com/) - контейнеризация
- [task](https://taskfile.dev/) - инструмент для автоматизации задач
- [sentry](https://sentry.io/) - мониторинг ошибок
- [prometheus](https://prometheus.io/) - мониторинг метрик

## Development

### Prerequisites

- Установить [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Установить [Docker](https://docs.docker.com/get-docker/)
- Установить [Task](https://taskfile.dev/installation/) или пользоваться `uvx --from go-task-bin task`


### Running locally

- Копируем `.example.env` в `.env` и заполняем переменные окружения
- Создаем виртуальное окружение и локальную базу данных: `task init`
- Запускаем локальный сервер: `task run`
- Если обновились миграции базы данных: `task upgrade-db`

## Environment

```bash
ENV=local|test|ci|dev|prod  # default: prod
APP_TITLE="Template Project"
APP_NAME=template_project
DEBUG=true

POSTGRES_HOST=localhost
POSTGRES_PORT=33432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=exampledb

SENTRY_DSN=https://sentry.io/your-dsn

PROMETHEUS_METRICS_KEY=secret
```

## API

Схема API или ссылка на Confluence.

## Quality control

### Pre-commit

Для автоматической проверки качества кода и авто-форматирования можно использовать `pre-commit`.

```bash
task pre-commit
```

### Linting and formatting

Для линтинга и форматирования кода используется `ruff`.

```bash
# проверить стиль кода форматирование
task lint

# автоматически применить рекомендованное форматирование
task format
```

### Type checking

Для проверки типов используется `mypy`.

```bash
task typecheck
```

### Tests

Для локальной работы тестов нужен запущенный Postgres.

```bash
# запуск Postgres на localhost:25434
docker compose up postgres-test

# или как демон
docker compose up -d postgres-test
```

После этого сами тесты можно запускать несколькими способами:

```bash
# через task
task test

# напрямую, например для вотчера
ENV=test uv run pytest
```

Для локальных тестов используется окружение из `.env.test`.
Для тестов в GitLab CI используется окружение из `.env.ci`.


## Project structure

```bash
$ tree "template_project"
template_project
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   ├── migrations  # Migrations
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── core  # configuration and library
├── schemas
├── api  # Package contains web server. Handlers, startup config.
│   ├── api_v1  # Package with all handlers.
│   └── router.py  # Main router.
└── tests  # Tests for project.
    └── conftest.py  # Fixtures for all tests.
```
