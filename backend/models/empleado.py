from sqlalchemy import Column, Integer, Boolean, DateTime, String
from sqlalchemy.orm import relationship
from datetime import timezone, datetime
from database import Base

class Empleados(Base):
    __tablename__ = "empleados"

    id_empleado  = Column(Integer,      primary_key=True, autoincrement=True)
    bio_id       = Column(String(20),   unique=True,  nullable=False)
    nombre       = Column(String(255),  nullable=False)
    cedula       = Column(String(20),   unique=True,  nullable=False)
    cargo        = Column(String(50),   nullable=True)
    area         = Column(String(50),   nullable=True)
    tarjeta_rfid = Column(String(100),  unique=True,  nullable=True)

    # ── Métodos registrados en el dispositivo ──
    tiene_huella   = Column(Boolean, default=False, nullable=False)
    tiene_password = Column(Boolean, default=False, nullable=False)  # ← nuevo

    # ── Métodos permitidos para marcar asistencia ──
    permite_huella   = Column(Boolean, default=True,  nullable=False)
    permite_rfid     = Column(Boolean, default=True,  nullable=False)
    permite_password = Column(Boolean, default=True,  nullable=False)  # ← nuevo

    activo    = Column(Boolean,  default=True, nullable=False)
    creado_en = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    registros = relationship("Registros", back_populates="empleado")