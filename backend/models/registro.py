from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from datetime import timezone, datetime
from database import Base
import enum

class MetodoAcceso(str, enum.Enum):
    huella           = "huella"
    password         = "password"
    rfid             = "rfid"
    huella_password  = "huella_password"
    huella_rfid      = "huella_rfid"
    desconocido      = "desconocido"

class TipoAcceso(str, enum.Enum):
    entrada = "entrada"
    salida  = "salida"

class Registros(Base):
    __tablename__ = "registros"

    id_registro    = Column(Integer,               primary_key=True, autoincrement=True)
    empleado_id    = Column(String(20),            ForeignKey("empleados.bio_id"), nullable=True)
    dispositivo_sn = Column(String(50),            nullable=True)
    metodo         = Column(Enum(MetodoAcceso),    nullable=False)
    tipo           = Column(Enum(TipoAcceso),      nullable=False)
    fecha_hora     = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    autorizado     = Column(Boolean,               default=True, nullable=False)
    motivo_bloqueo = Column(String(255),           nullable=True)
    creado_en      = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    empleado = relationship("Empleados", back_populates="registros")