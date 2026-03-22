from sqlalchemy import Column, Integer, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from  datetime import timezone, datetime
from database import Base

class Empleados(Base):
    __tablename__ = "empleados"

    id_empleado = Column(Integer, primary_key=True, autoincrement=True)  # PK → la asigna PostgreSQL
    bio_id      = Column(String(20), unique=True, nullable=False)  # UK → la asigna el biométrico
    nombre      = Column(String(255), nullable=False, unique=False)
    cedula      = Column(String(20), unique=True, nullable=False)
    cargo       = Column(String(50), nullable= True)
    area        = Column(String(50), nullable= True)
    tarjeta_rfid  = Column(String(100), unique=True, nullable=True)
    tiene_huella = Column(Boolean, default= False, nullable= False)
    permite_huella = Column(Boolean, default= True, nullable= False)
    permite_rfid = Column(Boolean, default= True, nullable= False)
    activo     = Column(Boolean, default=True, nullable=False)
    creado_en  = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    registros  = relationship("Registro", back_populates="empleado")
    
