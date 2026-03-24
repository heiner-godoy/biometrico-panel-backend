from fastapi import HTTPException, status, Depends, Path
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_usuario_actual
from models.usuario import Usuarios
from services.usuario import service_usuarios
from schemas.usuario import CreateUser, UpdateUser
from typing import List


def verificar_admin(usuario: Usuarios):
    if usuario.id_rol != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para esta acción"
        )


def get_usuarios(
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    return service_usuarios.get_usuarios(db)


def get_usuarios_activos(
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    return service_usuarios.get_usuario_activos(db)


def get_usuario_by_id(
    id_usuario: int   = Path(..., description="ID del usuario"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    resultado = service_usuarios.get_usuario_by_id(db, id_usuario)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return resultado


def get_usuario_by_email(
    email: str        = Path(..., description="Email del usuario"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    resultado = service_usuarios.get_usuario_by_email(db, email)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return resultado


def get_usuario_by_username(
    username: str     = Path(..., description="Username del usuario"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    resultado = service_usuarios.get_usuario_by_name(db, username)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return resultado


def create_usuario(
    data: CreateUser,
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    try:
        return service_usuarios.create_user(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def update_usuario(
    data: UpdateUser,
    id_usuario: int   = Path(..., description="ID del usuario"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    try:
        resultado = service_usuarios.update_user(db, id_usuario, data)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def delete_usuario(
    id_usuario: int   = Path(..., description="ID del usuario"),
    db: Session       = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    resultado = service_usuarios.delete_user(db, id_usuario)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return resultado