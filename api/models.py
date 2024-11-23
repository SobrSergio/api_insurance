from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Tariff(Base):
    __tablename__ = "tariffs"
    
    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String, index=True)
    rate = Column(Float, nullable=False)
    effective_date = Column(Date, nullable=False)

    
    tariff_group_id = Column(Integer, ForeignKey('tariff_groups.id'))

    
    tariff_group = relationship("TariffGroup", back_populates="tariffs")

    def __repr__(self):
        return f"<Tariff(id={self.id}, cargo_type={self.cargo_type}, rate={self.rate}, effective_date={self.effective_date})>"

class TariffGroup(Base):
    __tablename__ = "tariff_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    effective_date = Column(Date, nullable=False, unique=True)  

    
    tariffs = relationship("Tariff", back_populates="tariff_group")

    def __repr__(self):
        return f"<TariffGroup(id={self.id}, effective_date={self.effective_date})>"
