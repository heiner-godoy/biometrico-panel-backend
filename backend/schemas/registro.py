from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.registro import MetodoAcceso, TipoAcceso


class CreateRegistro(BaseModel):
    empleado_id:    str                    = Field(..., description="bio_id del empleado")
    dispositivo_sn: Optional[str]          = Field(None, max_length=50)
    metodo:         MetodoAcceso           = Field(..., description="huella | rfid | password | huella_rfid | huella_password")
    tipo:           TipoAcceso             = Field(..., description="entrada | salida")
    autorizado:     bool                   = True
    motivo_bloqueo: Optional[str]          = Field(None, max_length=255)


class ResponseRegistro(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_registro:    int
    empleado_id:    Optional[str]
    dispositivo_sn: Optional[str]
    fecha_hora:     datetime
    tipo:           TipoAcceso
    metodo:         MetodoAcceso
    autorizado:     bool
    motivo_bloqueo: Optional[str] = None
    creado_en:      datetime
    
class ResponseResumen(BaseModel):
    total_entradas:  int
    total_salidas:   int
    total_huella:    int
    total_rfid:      int
    total_password:  int
    total_bloqueados: int
    fecha:           datetime