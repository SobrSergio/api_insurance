from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import get_db, engine  # Импортируем функцию get_db

# Создаем таблицы в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/tariffs/", response_model=schemas.TariffResponse)
def create_tariff(tariff: schemas.TariffCreate, db: Session = Depends(get_db)):
    """
    Создает новый тариф.
    """
    return crud.create_tariff(db, tariff)

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
