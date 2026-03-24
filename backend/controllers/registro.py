from fastapi import HTTPException, status, Depends, Path, Query
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_usuario_actual
from models.usuario import Usuarios
from services.registro import service_registro
from schemas.registro import ResponseRegistro
from typing import List, Optional


def get_registros(
    metodo: Optional[str] = Query(None, description="huella | rfid | huella_rfid"),
    tipo: Optional[str]   = Query(None, description="entrada | salida"),
    db: Session           = Depends(get_db),
    usuario: Usuarios     = Depends(get_usuario_actual)
) -> List[ResponseRegistro]:
    return service_registro.get_registros(db)


def get_registro_by_id(
    id_registro: int  = Path(..., description="ID del registro"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
) -> ResponseRegistro:
    registro = service_registro.get_registro_by_id(db, id_registro)
    if not registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado"
        )
    return registro


def get_registros_by_empleado(
    bio_id: str       = Path(..., description="bio_id del empleado"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
) -> List[ResponseRegistro]:
    registros = service_registro.get_registros_by_empleado(db, bio_id)
    if not registros:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron registros para este empleado"
        )
    return registros


def get_registros_bloqueados(
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
) -> List[ResponseRegistro]:
    return service_registro.get_registros_bloqueados(db)