from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False, unique=True)

    usuarios = relationship("Usuarios", back_populates="rol")
