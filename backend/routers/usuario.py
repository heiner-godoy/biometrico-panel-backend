from fastapi import APIRouter, Depends
from controllers.usuario import (
    get_usuarios,
    get_usuarios_activos,
    get_usuario_by_id,
    get_usuario_by_email,
    get_usuario_by_username,
    create_usuario,
    update_usuario,
    delete_usuario
)
from schemas.usuario import ResponseUser
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[ResponseUser], status_code=200)
def listar(resultado=Depends(get_usuarios)):
    return resultado


@router.get("/activos", response_model=List[ResponseUser], status_code=200)
def listar_activos(resultado=Depends(get_usuarios_activos)):
    return resultado


@router.get("/id/{id_usuario}", response_model=ResponseUser, status_code=200)
def obtener_por_id(resultado=Depends(get_usuario_by_id)):
    return resultado


@router.get("/email/{email}", response_model=ResponseUser, status_code=200)
def obtener_por_email(resultado=Depends(get_usuario_by_email)):
    return resultado


@router.get("/username/{username}", response_model=ResponseUser, status_code=200)
def obtener_por_username(resultado=Depends(get_usuario_by_username)):
    return resultado


@router.post("/", response_model=ResponseUser, status_code=201)
def crear(resultado=Depends(create_usuario)):
    return resultado


@router.patch("/{id_usuario}", response_model=ResponseUser, status_code=200)
def actualizar(resultado=Depends(update_usuario)):
    return resultado


@router.delete("/{id_usuario}", response_model=ResponseUser, status_code=200)
def eliminar(resultado=Depends(delete_usuario)):
    return resultado
