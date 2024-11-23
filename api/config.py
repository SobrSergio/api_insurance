import warnings
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ValidationError

# Игнорируем предупреждения от Pydantic (задолбал)
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

class Settings(BaseSettings):
    """
    Класс для загрузки настроек из файла .env с помощью Pydantic.
    
    Загружает настройки из переменных окружения или файла .env,
    включая строку подключения к базе данных (database_url).
    """
    
    database_url: str

    class Config:
        """
        Конфигурация для Pydantic, чтобы указать путь к файлу .env
        """
        env_file = ".env"

    def __init__(self, **kwargs):
        """
        Инициализация класса Settings с загрузкой переменных окружения.

        Проверяет наличие файла .env и корректность значения для database_url.
        """
        try:
            super().__init__(**kwargs)
        except ValidationError as e:
            raise ValueError("Ошибка валидации настроек. Проверьте файл .env.") from e
        if not self.database_url:
            raise ValueError("Переменная окружения 'database_url' не задана.")

# Создаем объект настроек
try:
    settings = Settings()
except ValueError as e:
    print(f"Ошибка при загрузке настроек: {e}")
