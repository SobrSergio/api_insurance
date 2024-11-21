from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
from typing import Optional

def create_tariff(db: Session, tariff: schemas.TariffCreate) -> models.Tariff:
    """
    Создает новый тариф в базе данных.
    
    Args:
        db (Session): Сессия базы данных.
        tariff (schemas.TariffCreate): Данные для создания тарифа.
        
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
    except Exception as e:
        db.rollback()
        raise ValueError(f"Ошибка при создании тарифа: {e}")
    return db_tariff

def get_tariff(db: Session, tariff_id: int) -> Optional[models.Tariff]:
    """
    Получает тариф по ID.
    
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

def get_all_tariffs(db: Session) -> list[models.Tariff]:
    """
    Получает все тарифы из базы данных.
    
    Args:
        db (Session): Сессия базы данных.
        
    Returns:
        list[models.Tariff]: Список всех тарифов.
    """
    return db.query(models.Tariff).all()

def delete_tariff(db: Session, tariff_id: int) -> Optional[models.Tariff]:
    """
    Удаляет тариф по ID.
    
    Args:
        db (Session): Сессия базы данных.
        tariff_id (int): Идентификатор тарифа для удаления.
        
    Returns:
        Optional[models.Tariff]: Удаленный тариф или None, если тариф не найден.
    """
    tariff = get_tariff(db, tariff_id)
    if tariff:
        try:
            db.delete(tariff)
            db.commit()
        except Exception as e:
            db.rollback()
            raise ValueError(f"Ошибка при удалении тарифа: {e}")
    return tariff

def update_tariff(db: Session, tariff_id: int, updated_tariff: schemas.TariffUpdate) -> Optional[models.Tariff]:
    """
    Обновляет тариф по ID.
    
    Args:
        db (Session): Сессия базы данных.
        tariff_id (int): Идентификатор тарифа для обновления.
        updated_tariff (schemas.TariffUpdate): Данные для обновления тарифа.
        
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
        except Exception as e:
            db.rollback()
            raise ValueError(f"Ошибка при обновлении тарифа: {e}")
    return tariff

def calculate_insurance_cost(db: Session, cargo_type: str, declared_value: float, effective_date: date) -> float:
    """
    Рассчитывает стоимость страховки на основе актуального тарифа для типа груза и даты.
    
    Args:
        db (Session): Сессия базы данных.
        cargo_type (str): Тип груза.
        declared_value (float): Объявленная стоимость груза.
        effective_date (date): Дата страхования.
        
    Returns:
        float: Стоимость страховки.
        
    Raises:
        ValueError: Если тариф для указанного типа груза и даты не найден.
    """
    # Получаем актуальный тариф для данного типа груза и даты
    tariff = db.query(models.Tariff).filter(
        models.Tariff.cargo_type == cargo_type,
        models.Tariff.effective_date <= effective_date
    ).order_by(models.Tariff.effective_date.desc()).first()

    if not tariff:
        raise ValueError(f"Не найден тариф для типа груза '{cargo_type}' на дату {effective_date}.")

    # Рассчитываем стоимость страховки
    insurance_cost = declared_value * tariff.rate
    return insurance_cost