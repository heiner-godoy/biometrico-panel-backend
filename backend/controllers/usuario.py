from fastapi import HTTPException, status, Depends, Path
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_usuario_actual
from models.usuario import Usuarios
from services.usuario import service_usuarios
from schemas.usuario import CreateUser, ResponseUser, UpdateUser
from typing import List

def verificar_admin(usuario: Usuarios):
    if usuario.id_rol != 1:  # 1 = admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para esta acción"
        )

def get_usuarios_activos( db: Session = Depends(get_db), usuario: Usuarios = Depends(get_usuario_actual) )-> List[ResponseUser]:
        verificar_admin(usuario)  # Verificar permisos de admin
        try:
            return service_usuarios.get_usuario_activos(db)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)  # "Rol existente"
            )

def get_usuarios( db: Session = Depends(get_db), usuario: Usuarios = Depends(get_usuario_actual) )-> List[ResponseUser]:
        verificar_admin(usuario)  # Verificar permisos de admin
        try:
            return service_usuarios.get_usuarios(db)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)  # "Rol existente"
            )

def get_usuarios_by_id( db: Session = Depends(get_db),id_usuario: int = Path(..., description="ID del usuario a obtener"), usuario: Usuarios = Depends(get_usuario_actual) )-> ResponseUser:
        verificar_admin(usuario)  # Verificar permisos de admin
        try:
            return service_usuarios.get_usuario_by_id(db, id_usuario)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)  # "Rol existente"
            )

def get_usuarios_by_email( db: Session = Depends(get_db),email_usuario: str = Path(..., description="email del usuario a obtener"), usuario: Usuarios = Depends(get_usuario_actual) )-> ResponseUser:
        verificar_admin(usuario)  # Verificar permisos de admin
        try:
            return service_usuarios.get_usuario_by_email(db, email_usuario)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)  # "Rol existente"
            )
            
def get_usuarios_by_username( db: Session = Depends(get_db),username_usuario: str = Path(..., description="username del usuario a obtener"), usuario: Usuarios = Depends(get_usuario_actual) )-> ResponseUser:
        verificar_admin(usuario)  # Verificar permisos de admin
        try:
            return service_usuarios.get_usuario_by_name(db, username_usuario)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)  # "Rol existente"
            )


def create_usuarios(data:CreateUser, db: Session = Depends(get_db), usuario: Usuarios = Depends(get_usuario_actual) )-> ResponseUser:
        verificar_admin(usuario)  # Verificar permisos de admin
        try:
            return service_usuarios.create_user(db, data)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)  # "Rol existente"
            )
            
def update_usuario(data:UpdateUser, id:int = Path(..., description="Id del usuario a actualizar"), db: Session = Depends(get_db), usuario: Usuarios = Depends(get_usuario_actual) )-> ResponseUser:
        verificar_admin(usuario)  # Verificar permisos de admin
        try:
            return service_usuarios.update_user(db, id, data)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)  # "Rol existente"
            )

def delete_usuario(
    id: int = Path(..., description="id del usuario"),
    db: Session = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
) -> ResponseUser:
    verificar_admin(usuario)
    resultado = service_usuarios.delete_user(db, id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return resultado
