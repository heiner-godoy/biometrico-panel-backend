from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_usuario_actual
from models.usuario import Usuarios
from services.rol import service_rol
from schemas.rol import CreateRol, ResponseRol, UpdateRol
from typing import List

router = APIRouter(prefix="/roles", tags=["Roles"])

def verificar_admin(usuario: Usuarios):
    if usuario.id_rol != 1:  # 1 = admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para esta acción"
        )

# GET todos los roles
@router.get("/", response_model=List[ResponseRol], status_code=status.HTTP_200_OK)
def get_roles(
    db: Session = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    return service_rol.get_roles(db)

# GET un rol por ID
@router.get("/{id_rol}", response_model=ResponseRol, status_code=status.HTTP_200_OK)
def get_rol(
    id_rol: int = Path(..., description="ID del rol a obtener"),
    db: Session = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    rol = service_rol.get_rol_by_id(db, id_rol)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return rol

# POST crear un rol
@router.post("/", response_model=ResponseRol, status_code=status.HTTP_200_OK)
def create_rol(
    data: CreateRol,  # Datos del rol desde el cuerpo de la solicitud
    db: Session = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)  # Usuario para verificación de permisos
):
    verificar_admin(usuario)  # Verificar permisos de admin
    try:
        return service_rol.add_rol(db, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)  # "Rol existente"
        )

# PUT actualizar un rol
@router.put("/{id_rol}", response_model=ResponseRol, status_code=status.HTTP_200_OK)
def update_rol(
    data: UpdateRol,
    id_rol: int = Path(..., description="ID del rol a actualizar"),
    db: Session = Depends(get_db),
    usuario: Usuarios = Depends(get_usuario_actual)
):
    verificar_admin(usuario)
    rol = service_rol.update_rol(db, id_rol, data)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return rol

# DELETE eliminar un rol
@router.delete("/{id_rol}", response_model=ResponseRol, status_code=status.HTTP_200_OK)
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