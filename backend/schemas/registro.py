from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CreateRegistro(BaseModel):
    empleado_id:    str            = Field(..., description="bio_id del empleado")
    dispositivo_sn: Optional[str]  = Field(None, max_length=50)
    metodo:         str            = Field(..., min_length=3, max_length=20)
    tipo:           str            = Field(..., description="entrada o salida")
    autorizado:     bool = True
    motivo_bloqueo: Optional[str]  = Field(None, max_length=255)


class ResponseRegistro(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_registro:    int
    empleado_id:    Optional[str]
    dispositivo_sn: Optional[str]
    fecha_hora:     datetime
    tipo:           str
    metodo:         str
    autorizado:     bool
    motivo_bloqueo: Optional[str] = None
    creado_en:      datetime