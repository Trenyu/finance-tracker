from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Gasto(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    categoria = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
