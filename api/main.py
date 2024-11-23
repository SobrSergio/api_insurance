from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import get_db, engine  # Импортируем функцию get_db

# Создаем таблицы в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/tariffs/", response_model=schemas.TariffResponse)
def create_tariff(
    tariff: schemas.TariffCreate, 
    db: Session = Depends(get_db)
):
    """
    Создает новый тариф (старая структура).
    """
    return crud.create_tariff(db, tariff)

@app.post("/tariffs/by_date/", response_model=dict)
def create_tariffs_by_date(
    tariffs_by_date: schemas.TariffsByDateCreate, 
    db: Session = Depends(get_db)
):
    """
    Создает тарифы по датам (новая структура).
    """
    crud.create_tariffs_by_date(db, tariffs_by_date)
    return {"message": "Tariffs created successfully"}


@app.get("/")
def main():
    """
    Простой endpoint для проверки работоспособности сервиса.
    """
    return {"message": "Hello World!"}

@app.get("/tariffs/", response_model=list[schemas.TariffResponse])
def read_tariffs(db: Session = Depends(get_db)):
    """
    Получает все тарифы из базы данных.
    """
    return crud.get_all_tariffs(db)

@app.delete("/tariffs/{tariff_id}", response_model=schemas.TariffResponse)
def delete_tariff(tariff_id: int, db: Session = Depends(get_db)):
    """
    Удаляет тариф по его ID.
    """
    deleted = crud.delete_tariff(db, tariff_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return deleted

@app.put("/tariffs/{tariff_id}", response_model=schemas.TariffResponse)
def update_tariff(tariff_id: int, tariff: schemas.TariffUpdate, db: Session = Depends(get_db)):
    """
    Обновляет тариф по его ID.
    """
    updated = crud.update_tariff(db, tariff_id, tariff)
    if not updated:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return updated

@app.get("/tariffs/by_date", response_model=dict)
def get_tariffs_structured(db: Session = Depends(get_db)):
    """
    Получает тарифы из базы данных, возвращая их в структуре, где ключами являются даты, а значениями — тарифы.
    """
    tariffs = crud.get_all_tariffs(db)
    
    structured_tariffs = {}
    
    for tariff in tariffs:
        # Группируем тарифы по effective_date
        date_str = tariff.effective_date.isoformat()  # Преобразуем дату в строку
        if date_str not in structured_tariffs:
            structured_tariffs[date_str] = []
        
        structured_tariffs[date_str].append({
            "cargo_type": tariff.cargo_type,
            "rate": tariff.rate,
            "effective_date": date_str,
        })
    
    return structured_tariffs

# Новый метод для расчета стоимости страхования
@app.post("/insurance/", response_model=schemas.InsuranceResponse)
def calculate_insurance(insurance_request: schemas.InsuranceRequest, db: Session = Depends(get_db)):
    """
    Расчитывает стоимость страхования на основе типа груза и заявленной стоимости.
    """
    insurance_cost = crud.calculate_insurance_cost(
        db=db,
        cargo_type=insurance_request.cargo_type,
        declared_value=insurance_request.declared_value,
        effective_date=insurance_request.effective_date
    )

    if insurance_cost == 0.0:
        raise HTTPException(status_code=404, detail="Tariff not found for the given cargo type and date")

    return schemas.InsuranceResponse(
        cargo_type=insurance_request.cargo_type,
        declared_value=insurance_request.declared_value,
        insurance_cost=insurance_cost
    )
