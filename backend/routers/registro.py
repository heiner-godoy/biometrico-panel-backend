from fastapi import APIRouter, Depends
from controllers.registro import (
    get_registros,
    get_registro_by_id,
    get_registros_by_empleado,
    get_registros_bloqueados,
    get_resumen_dia        # ← nuevo
)
from schemas.registro import ResponseRegistro, ResponseResumen  # ← nuevo
from typing import List

router = APIRouter(prefix="/registros", tags=["Registros"])


@router.get("/", response_model=List[ResponseRegistro], status_code=200)
def listar(resultado=Depends(get_registros)):
    return resultado


@router.get("/resumen", status_code=200)
def resumen_dia(resultado=Depends(get_resumen_dia)):
    return resultado


@router.get("/bloqueados", response_model=List[ResponseRegistro], status_code=200)
def listar_bloqueados(resultado=Depends(get_registros_bloqueados)):
    return resultado


@router.get("/id/{id_registro}", response_model=ResponseRegistro, status_code=200)
def obtener(resultado=Depends(get_registro_by_id)):
    return resultado


@router.get("/empleado/{bio_id}", response_model=List[ResponseRegistro], status_code=200)
def obtener_por_empleado(resultado=Depends(get_registros_by_empleado)):
    return resultado