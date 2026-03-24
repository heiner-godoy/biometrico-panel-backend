# routers/rol_router.py
from fastapi import APIRouter, Depends
from controllers.rol import (
    get_roles,
    get_rol,
    create_rol,
    update_rol,
    delete_rol
)
from schemas.rol import ResponseRol
from typing import List

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/",          response_model=List[ResponseRol])
def listar(resultado=Depends(get_roles)):
    return resultado

@router.get("/{id_rol}",  response_model=ResponseRol)
def obtener(resultado=Depends(get_rol)):
    return resultado

@router.post("/",         response_model=ResponseRol, status_code=201)
def crear(resultado=Depends(create_rol)):
    return resultado

@router.patch("/{id_rol}", response_model=ResponseRol)
def actualizar(resultado=Depends(update_rol)):
    return resultado

@router.delete("/{id_rol}")
def eliminar(resultado=Depends(delete_rol)):
    return resultado