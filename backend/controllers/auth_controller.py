from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_usuario_actual
from core.security import verify_password, crear_token
from models.usuario import Usuarios
from schemas.usuario import ResponseUser


def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 1. buscar el usuario por username
    usuario = db.query(Usuarios).filter(
        Usuarios.username == form.username
    ).first()

    # 2. verificar que existe
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    # 3. verificar contraseña
    if not verify_password(form.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )

    # 4. verificar que está activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    # 5. generar el JWT
    token = crear_token({
        "sub": usuario.username,
        "rol": usuario.id_rol,
        "id":  usuario.id_usuario
    })

    # 6. retornar el token — formato estándar OAuth2
    return {
        "access_token": token,
        "token_type":   "bearer",
        "rol":          usuario.id_rol,
        "username":     usuario.username
    }


def me(
    usuario: Usuarios = Depends(get_usuario_actual)
) -> ResponseUser:
    return usuario
