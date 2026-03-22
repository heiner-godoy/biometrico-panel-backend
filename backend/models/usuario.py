from sqlalchemy import Column, DateTime, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import timezone, datetime
from database import Base



class Usuarios(Base):
    __tablename__ = "usuarios"

    id_usuario  = Column(Integer, primary_key=True, autoincrement=True)
    id_rol      = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)
    username    = Column(String(20), unique=True, nullable=False, )
    email       = Column(String(100), unique=True, nullable=False, index=True)
    password    = Column(String(100), nullable=False)
    activo      = Column(Boolean, default=True, nullable=False)
    creado_en   = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ultimo_login = Column(DateTime, nullable=True)

    rol = relationship("Rol", back_populates="usuarios")
