
# REST API для расчета стоимости страхования

Реализовать REST API сервис по расчёту стоимости страхования в зависимости от типа груза и объявленной стоимости (ОС).

## Структура проекта

Проект реализован с использованием следующих технологий:
- **FastAPI** - фреймворк для создания веб-приложений.
- **SQLAlchemy ORM** - для работы с базой данных.
- **PostgreSQL** - реляционная база данных.
- **Docker и Docker Compose** - для контейнеризации и управления средой.
- **Kafka** - для логгирования изменений тарифов.

## Основные возможности (все реализованно точно также, как сказано в тз.)

1. **Загрузка тарифных данных**: 
    - Данные тарифов загружаются из JSON-файла или аналогичной структуры через API и сохраняются в базе данных.

2. **CRUD-операции для тарифов**:
    - Создание новых тарифов.
    - Обновление существующих тарифов.
    - Удаление тарифов.

3. **Расчет стоимости страхования**:
    - Рассчитывается на основе типа груза и заявленной стоимости.

4. **Логирование изменений** (будущая функциональность):
    - Логирование действий с тарифами через Kafka с сохранением данных о:
      - ID пользователя (при наличии).
      - Типе действия.
      - Метке времени.

## Установка и запуск

1. **Клонируйте репозиторий**:
    ```bash
    git clone https://github.com/SobrSergio/api_insurance
    cd insurance-api
    ```

2. **Создайте файл `.env`**:
    Создайте файл `.env` в корне проекта и добавьте в него настройки подключения к базе данных
    DATABASE_URL=(вставьте ссылку)
    Я не стал выносить всё в .env

3. **Запустите Docker Compose**:
    ```bash
    docker-compose up --build
    ```
4. **Запуск сервиса**:
    Откройте браузер и перейдите по адресу `http://127.0.0.1:8000/docs` для доступа к документации API.
    Так же можно увидить kafdrop (удобно для просмотра сообщений и анализа kafka) по дарсе `http://127.0.0.1:9000`


## Структура JSON для загрузки тарифов (можно и через дату как в тз - это просто пример (посмотрите через Swagger))

```json
[
    {
        "cargo_type": "electronics",
        "rate": 0.05
    },
    {
        "cargo_type": "furniture",
        "rate": 0.02
    }
]
```

## Будущие улучшения

1. **Логирование**:
    - Добавить полноценное логирование всех действий.

2. **Конфигурация через `.env`**:
    - Вынести все конфигурационные параметры в файл `.env` для улучшения управляемости.