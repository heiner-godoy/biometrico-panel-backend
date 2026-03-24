from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from  datetime import timezone, datetime
from test.database import Base

class Registros(Base):
    __tablename__ = "registros"
    id_registro = Column(Integer, primary_key= True, autoincrement=True)
    empleado_id = Column(String(20), ForeignKey("empleados.bio_id"), nullable=True)
    dispositivo_sn = Column(String(50), nullable= True)
    metodo = Column(String(20), nullable= False, unique= False)
    fecha_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    tipo = Column(String(20), nullable= False )
    autorizado = Column(Boolean, default=True, nullable= False)
    motivo_bloqueo = Column(String(255), nullable= True )
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    empleado = relationship("Empleados", back_populates="registros")