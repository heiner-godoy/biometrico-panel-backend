from fastapi import HTTPException, status, Depends, Path
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_usuario_actual
from models.usuario import Usuarios
from services.empleado import empleado_service
from schemas.empleado import CreateEmpleado, ResponseEmpleado, UpdateEmpleado
from typing import List


def verificar_admin(usuario: Usuarios):
    if usuario.id_rol != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para esta acción"
        )


def get_empleados(
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    return empleado_service.get_empleados(db)


def get_empleado_by_id(
    bio_id: str       = Path(..., description="bio_id del empleado"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    empleado = empleado_service.get_empleado_by_id(db, bio_id)
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    return empleado


def get_empleado_by_cedula(
    cedula: str       = Path(..., description="Cédula del empleado"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    empleado = empleado_service.get_empleado_by_cedula(db, cedula)
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    return empleado


def create_empleado(
    data: CreateEmpleado,
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    try:
        return empleado_service.add_empleado(db, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


def update_empleado(
    data: UpdateEmpleado,
    bio_id: str       = Path(..., description="bio_id del empleado"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    try:
        empleado = empleado_service.update_empleado(db, bio_id, data)
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        return empleado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


def delete_empleado(
    bio_id: str       = Path(..., description="bio_id del empleado"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    empleado = empleado_service.delete_empleado(db, bio_id)
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    return empleado