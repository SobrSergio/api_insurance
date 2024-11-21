from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

class CargoTypeEnum(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    furniture = "furniture"

class TariffCreate(BaseModel):
    cargo_type: CargoTypeEnum = Field(..., description="Тип груза")
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
