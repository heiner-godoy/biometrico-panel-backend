from fastapi import HTTPException, status, Depends, Path
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_usuario_actual
from models.usuario import Usuarios
from services.rol import service_rol
from schemas.rol import CreateRol, ResponseRol, UpdateRol
from typing import List

def verificar_admin(usuario: Usuarios):
    if usuario.id_rol != 1:  # 1 = admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para esta acción"
        )

# GET todos los roles
def get_roles(
    db: Session = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
) -> List[ResponseRol]:
    return service_rol.get_roles(db)

# GET un rol por ID
def get_rol(
    id_rol: int = Path(..., description="ID del rol a obtener"),
    db: Session = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
) -> ResponseRol:
    rol = service_rol.get_rol_by_id(db, id_rol)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return rol

# POST crear un rol
def create_rol(
    data: CreateRol,  # Datos del rol desde el cuerpo de la solicitud
    db: Session = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)  # Usuario para verificación de permisos
) -> ResponseRol:
    verificar_admin(usuario)  # Verificar permisos de admin
    try:
        return service_rol.add_rol(db, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)  # "Rol existente"
        )

# PUT actualizar un rol
def update_rol(
    data: UpdateRol,
    id_rol: int = Path(..., description="ID del rol a actualizar"),
    db: Session = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
) -> ResponseRol:
    verificar_admin(usuario)
    rol = service_rol.update_rol(db, id_rol, data)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return rol

# DELETE eliminar un rol
def delete_rol(
    id_rol: int = Path(..., description="ID del rol a eliminar"),
    db: Session = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    rol = service_rol.delete_rol(db, id_rol)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return {"message": "Rol eliminado exitosamente"}