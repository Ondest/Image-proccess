Этот репозиторий решение [вот этого](https://docs.google.com/document/d/1yKpCTUkmPjZdsn_srsnkUHzfMFVLhB_xY-bNxCkrAv4/edit?tab=t.0#heading=h.h6p7sxav6vp8) технического задания.

**image_process_app** выполняет функцию обработки фотографий.
Зависимости:

```toml
python = "^3.12"
aiokafka = "^0.12.0"
pillow = "^11.0.0"
python-dotenv = "^1.0.1"
```

**image_app** это api для фотографий

Зависимости:

```toml
python = "^3.12"
fastapi = "^0.115.4"
uvicorn = "^0.32.0"
asyncpg = "^0.30.0"
sqlalchemy = "^2.0.36"
alembic = "^1.13.3"
pydantic-settings = "^2.6.1"
black = "^24.10.0"
pytest-asyncio = "0.23.6"
pytest = "8.1.1"
httpx = "^0.27.2"
fastapi-cache2 = {extras = ["redis"], version = "^0.2.2"}
python-multipart = "^0.0.17"
aiofiles = "^24.1.0"
aiokafka = "^0.12.0"
pyjwt = {extras = ["crypto"], version = "^2.9.0"}
bcrypt = "^4.2.0"
pydantic = {extras = ["email"], version = "^2.9.2"}
```

### Инструкция к запуску

Сначала нужно подготовить приложениe **image_app**

1. Внутри директории **image__app** воспользоваться командой `make certs`
2. Должна появиться директория **certs** и в ней **public.pem** и **private.pem**
3. Создать **.env** файл на основе **.env-example**

Следующим шагом подготовка приложения **image_process_app**

- Требуется только создать **.env** файл на основе **.env-example**

Запустить приложение можно через команду

```bash
docker compose --env-file ./image_app/.env up --build -d
```
Нужно прогнать миграции командой `make migrate`

[Swagger](http://127.0.0.1:8000/)

Порты:

- 8000 image_app
- 10101 image_process_app
- 5432 postgres
- 6379 redis
- 2181 zookeeper
- 9092 и 9093 kafka

Структура **image_app**

```bash
├── image_app
│   ├── alembic.ini
│   ├── app
│   │   ├── api      # Точка входа и эндпоинты
│   │   ├── certs    # Ключи шифрования
│   │   ├── core     # Инфраструктурный слой
│   │   ├── db       # SQlALchemy, Redis
│   │   ├── kafka
│   │   ├── schemas  # Pydantic схемы
│   │   ├── services # Бизнес логика
│   │   └── static   # Файлы фотографий
│   ├── Dockerfile
│   ├── Makefile
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── tests
```

Тесты можно прогнать командой `make test` при запущенных контейнерах. При выполнении задания столкнулся с плавающим багом пакета `pytest.asyncio`который иногда не может прочитать 1ый тест из за какой то ошибки инициализации вот [тикет](https://github.com/pytest-dev/pytest-asyncio/issues/830), проблему решить перебором пакетов решить не удалось, так что иногда первый тест может падать, но он ничего не тестирует

### Комментарии

- PEP8 соблюден и проверен за счет пакета `black`
- Пароли и пользователи лежат в Redis, там же будет лежать кэш на запросы **get_image** и **get_images**
- Pillow выбрана как выбрана как самая подходящая библиотека для указанных действий с фотографиями
- Aiokafka была выбрана как одно из популярных асинхронных решений, но выбор не самый удачный оказался, для этой задачи по моему мнению лучше бы подошла библиотека faststream, до этого с kafka не работал
