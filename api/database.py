from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

# Создаем подключение к базе данных
try:
    engine = create_engine(settings.database_url)
except Exception as e:
    logger.error(f"Ошибка при подключении к базе данных: {e}")
    raise

# Сессия для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Основной класс для декларативной базы
Base = declarative_base()

def get_db():
    """
    Dependency для получения сессии с базой данных.
    
    Создает сессию базы данных и гарантирует, что она будет закрыта после использования.
    
    Returns:
        Session: Сессия базы данных для выполнения операций.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
