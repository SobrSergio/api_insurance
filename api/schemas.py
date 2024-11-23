from pydantic import BaseModel, Field, root_validator
from datetime import date
from typing import List, Dict

class TariffCreate(BaseModel):
    cargo_type: str = Field(..., description="Тип груза")
    rate: float = Field(..., ge=0, description="Тариф за единицу груза")
    effective_date: date = Field(..., description="Дата вступления тарифа в силу")

class TariffUpdate(BaseModel):
    cargo_type: str = Field(..., description="Тип груза", min_length=1)
    rate: float = Field(..., ge=0, description="Тариф за единицу груза")
    effective_date: date = Field(..., description="Дата вступления тарифа в силу")

class TariffResponse(TariffCreate):
    id: int

    class Config:
        orm_mode = True

class TariffsByDateResponse(BaseModel):
    tariffs_by_date: Dict[date, List[TariffCreate]]

    class Config:
        orm_mode = True

class TariffsByDateCreate(BaseModel):
    tariffs_by_date: Dict[date, List[TariffCreate]]
    
    @root_validator(pre=True)
    def add_effective_date(cls, values):
        """Добавляет поле effective_date в каждый тариф."""
        if "tariffs_by_date" in values:
            processed = {}
            for effective_date, tariffs in values["tariffs_by_date"].items():
                updated_tariffs = [
                    {**tariff, "effective_date": effective_date} for tariff in tariffs
                ]
                processed[effective_date] = updated_tariffs
            values["tariffs_by_date"] = processed
        return values

    class Config:
        orm_mode = True

# Новые схемы для расчета стоимости страхования
class InsuranceRequest(BaseModel):
    cargo_type: str
    declared_value: float
    effective_date: date

class InsuranceResponse(BaseModel):
    cargo_type: str
    declared_value: float
    insurance_cost: float

    class Config:
        orm_mode = True
