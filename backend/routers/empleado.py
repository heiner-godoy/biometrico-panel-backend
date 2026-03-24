from fastapi import APIRouter, Depends
from controllers.empleado import (
    get_empleados,
    get_empleado_by_id,
    get_empleado_by_cedula,
    create_empleado,
    update_empleado,
    delete_empleado
)
from schemas.empleado import ResponseEmpleado
from typing import List

router = APIRouter(prefix="/empleados", tags=["Empleados"])


@router.get("/", response_model=List[ResponseEmpleado], status_code=200)
def listar(resultado=Depends(get_empleados)):
    return resultado


@router.get("/bio/{bio_id}", response_model=ResponseEmpleado, status_code=200)
def obtener_por_bio(resultado=Depends(get_empleado_by_id)):
    return resultado


@router.get("/cedula/{cedula}", response_model=ResponseEmpleado, status_code=200)
def obtener_por_cedula(resultado=Depends(get_empleado_by_cedula)):
    return resultado


@router.post("/", response_model=ResponseEmpleado, status_code=201)
def crear(resultado=Depends(create_empleado)):
    return resultado


@router.patch("/{bio_id}", response_model=ResponseEmpleado, status_code=200)
def actualizar(resultado=Depends(update_empleado)):
    return resultado


@router.delete("/{bio_id}", response_model=ResponseEmpleado, status_code=200)
def eliminar(resultado=Depends(delete_empleado)):
    return resultado
