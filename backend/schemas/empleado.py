from pydantic import Field , BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CreateEmpleado(BaseModel):
    bio_id : str = Field(..., max_length=20, description="UK → la asigna el biométrico" ) 
    nombre : str = Field(..., max_length=255, description="nombre del empleado")
    cedula : str = Field(..., max_length= 20, description="Identificacion del empleado")
    cargo  : Optional[str] = Field (None, max_length=50, description= "Cargo del empleado")
    area   : Optional[str] = Field (None, max_length=50, description= "Area del empleado") 
    tarjeta_rfid : Optional[str] = Field (None, max_length=100, description= "tarjeta de acceso")
    tiene_huella : bool = False
    permite_huella : bool = True
    permite_rfid : bool = True
    activo : bool = True


class ResponseEmpleado(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    id_empleado : int 
    bio_id : str
    nombre : str
    cedula : str
    cargo : Optional[str]
    area : Optional[str]
    tarjeta_rfid : Optional[str]
    tiene_huella : bool
    permite_rfid : bool
    activo : bool
    creado_en : datetime

class UpdateEmpleado(BaseModel):
    nombre:         Optional[str] = None
    cargo:          Optional[str] = None
    area:           Optional[str] = None
    tarjeta_rfid:   Optional[str] = None
    tiene_huella:   Optional[bool] = None
    permite_huella: Optional[bool] = None
    permite_rfid:   Optional[bool] = None
    activo:         Optional[bool] = None