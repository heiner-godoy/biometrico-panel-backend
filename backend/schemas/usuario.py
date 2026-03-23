import re
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime

class CreateUser(BaseModel):
    id_rol : int = Field(..., description="id del rol del usuario")
    username: str = Field(..., max_length=20, description="Nombre del usuario del panel")
    email : str =  Field(..., description="Correo del usuario")
    password: str = Field(..., min_length= 6, description="Contraseña del usuario")

    
    @field_validator('email')
    @classmethod
    def validate_correo(cls, value):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(pattern, value):
            raise ValueError('Correo inválido')
        return value.lower()
    
    
class ResponseUser(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    
    id_usuario : int
    username : str
    email : str
    activo : bool
    creado_en : datetime
    ultimo_login : Optional[datetime]
    
class UpdateUser(BaseModel):
    username:  Optional[str] = None
    email:     Optional[str] = None
    password:  Optional[str] = None
    activo:    Optional[bool] = None
    id_rol:    Optional[int] = None
    
    @field_validator('email')
    @classmethod
    def validate_correo(cls, value):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(pattern, value):
            raise ValueError('Correo inválido')
        return value.lower()
