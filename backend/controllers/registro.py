from fastapi import HTTPException, status, Depends, Path, Query
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_usuario_actual
from models.usuario import Usuarios
from models.registro import MetodoAcceso, TipoAcceso
from services.registro import service_registro
from schemas.registro import ResponseRegistro
from typing import List, Optional



def get_registros(
    metodo:          Optional[MetodoAcceso] = Query(None, description="huella | rfid | password | huella_rfid | huella_password"),
    tipo:            Optional[TipoAcceso]   = Query(None, description="entrada | salida"),
    solo_bloqueados: Optional[bool]         = Query(None, description="Solo registros no autorizados"),
    empleado_id:     Optional[str]          = Query(None, description="bio_id del empleado"),
    fecha_desde:     Optional[str]          = Query(None, description="Fecha inicio YYYY-MM-DD"),
    fecha_hasta:     Optional[str]          = Query(None, description="Fecha fin YYYY-MM-DD"),
    limite:          int                    = Query(100, le=1000, description="Máximo de resultados"),
    db: Session      = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    # Ahora sí se pasan los filtros al servicio
    return service_registro.get_registros(
        db,
        metodo=metodo,
        tipo=tipo,
        solo_bloqueados=solo_bloqueados,
        empleado_id=empleado_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        limite=limite,
    )


def get_registro_by_id(
    id_registro: int  = Path(..., description="ID del registro"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
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
):
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
):
    return service_registro.get_registros_bloqueados(db)

def get_resumen_dia(
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    return service_registro.get_resumen_dia(db)