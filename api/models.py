from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint
from .database import Base

class Tariff(Base):
    __tablename__ = "tariffs"
    
    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String, index=True)
    rate = Column(Float, nullable=False)
    effective_date = Column(Date, nullable=False)

    # Добавляем уникальное ограничение на cargo_type и effective_date
    __table_args__ = (
        UniqueConstraint('cargo_type', 'effective_date', name='uix_cargo_type_effective_date'),
    )

    def __repr__(self):
        return f"<Tariff(id={self.id}, cargo_type={self.cargo_type}, rate={self.rate}, effective_date={self.effective_date})>"
