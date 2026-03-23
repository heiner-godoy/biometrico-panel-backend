from pydantic import BaseModel, Field, ConfigDict

class CreateRol(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="nombre del rol")
    
class ResponseRol(BaseModel):
    model_config =ConfigDict(from_attributes=True)
    id_rol: int
    nombre: str

