from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
from typing import Optional, Dict, List
from .kafka_file import send_to_kafka  # Импортируем функцию для отправки сообщений в Kafka

# Создание тарифов для старой структуры
def create_tariff(db: Session, tariff: schemas.TariffCreate, user_id: Optional[int] = None) -> models.Tariff:
    """
    Создает новый тариф в базе данных и отправляет лог в Kafka для старой структуры.
    
    Args:
        db (Session): Сессия базы данных.
        tariff (schemas.TariffCreate): Данные для создания тарифа.
        user_id (Optional[int]): ID пользователя, который совершает действие (если есть).
        
    Returns:
        models.Tariff: Созданный тариф.
    """
    db_tariff = models.Tariff(
        cargo_type=tariff.cargo_type,
        rate=tariff.rate,
        effective_date=tariff.effective_date,
    )
    try:
        db.add(db_tariff)
        db.commit()
        db.refresh(db_tariff)

        # Логирование в Kafka
        message = {
            "user_id": user_id,
            "action": "create_tariff",
            "tariff_id": db_tariff.id,
            "cargo_type": db_tariff.cargo_type,
            "rate": db_tariff.rate,
            "effective_date": db_tariff.effective_date.isoformat(),
            "timestamp": db_tariff.effective_date.isoformat(),
        }
        send_to_kafka(message)

    except Exception as e:
        db.rollback()
        raise ValueError(f"Ошибка при создании тарифа: {e}")
    
    return db_tariff

# Получение тарифа по ID для старой структуры
def get_tariff(db: Session, tariff_id: int) -> Optional[models.Tariff]:
    """
    Получает тариф по ID для старой структуры.
    
    Args:
        db (Session): Сессия базы данных.
        tariff_id (int): Идентификатор тарифа.
        
    Returns:
        Optional[models.Tariff]: Тариф, если найден, иначе None.
    """
    tariff = db.query(models.Tariff).filter(models.Tariff.id == tariff_id).first()
    if not tariff:
        raise ValueError(f"Тариф с ID {tariff_id} не найден.")
    return tariff

# Получение всех тарифов для старой структуры
def get_all_tariffs(db: Session) -> list[models.Tariff]:
    """
    Получает все тарифы из базы данных для старой структуры.
    
    Args:
        db (Session): Сессия базы данных.
        
    Returns:
        list[models.Tariff]: Список всех тарифов.
    """
    return db.query(models.Tariff).all()

# Удаление тарифа для старой структуры
def delete_tariff(db: Session, tariff_id: int, user_id: Optional[int] = None) -> Optional[models.Tariff]:
    """
    Удаляет тариф по ID и отправляет лог в Kafka для старой структуры.
    
    Args:
        db (Session): Сессия базы данных.
        tariff_id (int): Идентификатор тарифа для удаления.
        user_id (Optional[int]): ID пользователя, который совершает действие (если есть).
        
    Returns:
        Optional[models.Tariff]: Удаленный тариф или None, если тариф не найден.
    """
    tariff = get_tariff(db, tariff_id)
    if tariff:
        try:
            db.delete(tariff)
            db.commit()

            # Логирование в Kafka
            message = {
                "user_id": user_id,
                "action": "delete_tariff",
                "tariff_id": tariff.id,
                "cargo_type": tariff.cargo_type,
                "rate": tariff.rate,
                "effective_date": tariff.effective_date.isoformat(),
                "timestamp": tariff.effective_date.isoformat(),
            }
            send_to_kafka(message)

        except Exception as e:
            db.rollback()
            raise ValueError(f"Ошибка при удалении тарифа: {e}")
    return tariff

# Обновление тарифа для старой структуры
def update_tariff(db: Session, tariff_id: int, updated_tariff: schemas.TariffUpdate, user_id: Optional[int] = None) -> Optional[models.Tariff]:
    """
    Обновляет тариф по ID и отправляет лог в Kafka для старой структуры.
    
    Args:
        db (Session): Сессия базы данных.
        tariff_id (int): Идентификатор тарифа для обновления.
        updated_tariff (schemas.TariffUpdate): Данные для обновления тарифа.
        user_id (Optional[int]): ID пользователя, который совершает действие (если есть).
        
    Returns:
        Optional[models.Tariff]: Обновленный тариф, если он был найден и обновлен.
    """
    tariff = get_tariff(db, tariff_id)
    if tariff:
        tariff.cargo_type = updated_tariff.cargo_type
        tariff.rate = updated_tariff.rate
        tariff.effective_date = updated_tariff.effective_date
        try:
            db.commit()
            db.refresh(tariff)

            # Логирование в Kafka
            message = {
                "user_id": user_id,
                "action": "update_tariff",
                "tariff_id": tariff.id,
                "cargo_type": tariff.cargo_type,
                "rate": tariff.rate,
                "effective_date": tariff.effective_date.isoformat(),
                "timestamp": tariff.effective_date.isoformat(),
            }
            send_to_kafka(message)

        except Exception as e:
            db.rollback()
            raise ValueError(f"Ошибка при обновлении тарифа: {e}")
    return tariff

# Создание тарифов по группам дат и типов грузов для новой структуры
def create_tariffs_by_date(db: Session, tariffs_by_date: schemas.TariffsByDateCreate, user_id: Optional[int] = None):
    """
    Создает новые тарифы по группам дат и типов грузов для новой структуры.
    
    Args:
        db (Session): Сессия базы данных.
        tariffs_by_date (schemas.TariffsByDateCreate): Данные для создания тарифов.
        user_id (Optional[int]): ID пользователя, который совершает действие (если есть).
    """
    try:
        for effective_date, tariffs in tariffs_by_date.tariffs_by_date.items():
            for tariff in tariffs:
                db_tariff = models.Tariff(
                    cargo_type=tariff.cargo_type,
                    rate=tariff.rate,
                    effective_date=effective_date,
                )
                db.add(db_tariff)

        db.commit()

        # Логирование в Kafka
        for effective_date, tariffs in tariffs_by_date.tariffs_by_date.items():
            for tariff in tariffs:
                message = {
                    "user_id": user_id,
                    "action": "create_tariff",
                    "cargo_type": tariff.cargo_type,
                    "rate": tariff.rate,
                    "effective_date": effective_date.isoformat(),
                    "timestamp": effective_date.isoformat(),
                }
                send_to_kafka(message)

    except Exception as e:
        db.rollback()
        raise ValueError(f"Ошибка при создании тарифов: {e}")

# Получение тарифов для конкретной даты для новой структуры
def get_tariffs_by_date(db: Session, effective_date: date) -> Dict[date, List[models.Tariff]]:
    """
    Получает тарифы для конкретной даты для новой структуры.
    
    Args:
        db (Session): Сессия базы данных.
        effective_date (date): Дата для поиска тарифов.
        
    Returns:
        Dict[date, List[models.Tariff]]: Словарь с датами и списками тарифов.
    """
    tariffs = db.query(models.Tariff).filter(models.Tariff.effective_date == effective_date).all()
    if not tariffs:
        raise ValueError(f"Тарифы на дату {effective_date} не найдены.")
    
    tariffs_by_date = {effective_date: tariffs}
    return tariffs_by_date
