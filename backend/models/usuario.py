from sqlalchemy import Column, DateTime, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import timezone, datetime
from test.database import Base
from models.rol import Rol   # 👈 importa la clase Rol

class Usuarios(Base):
    __tablename__ = "usuarios"

    id_usuario  = Column(Integer, primary_key=True, autoincrement=True)
    id_rol      = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)
    username    = Column(String(20), unique=True, nullable=False)
    email       = Column(String(100), unique=True, nullable=False, index=True)
    password    = Column(String(255), nullable=False)   # 👈 ya corregido
    activo      = Column(Boolean, default=True, nullable=False)
    creado_en   = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ultimo_login = Column(DateTime, nullable=True)

    rol = relationship("Rol", back_populates="usuarios")