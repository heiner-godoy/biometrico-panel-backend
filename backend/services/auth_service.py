from sqlalchemy.orm import Session
from models.usuario import Usuarios
from core.security import verify_password, crear_token, verificar_token


def login(db: Session, username: str, password: str):
    # 1. buscar el usuario
    usuario = db.query(Usuarios).filter(
        Usuarios.username == username
    ).first()

    # 2. verificar que existe
    if not usuario:
        raise ValueError("Usuario no encontrado")

    # 3. verificar contraseña
    if not verify_password(password, usuario.password):
        raise ValueError("Contraseña incorrecta")

    # 4. verificar que está activo
    if not usuario.activo:
        raise ValueError("Usuario inactivo")

    # 5. generar el JWT con los datos del usuario
    token = crear_token({
        "sub": usuario.username,    # sub = subject (quién es)
        "rol": usuario.id_rol,      # rol para permisos
        "id":  usuario.id_usuario   # id para buscarlo después
    })

    return {"access_token": token, "token_type": "bearer"}


def get_usuario_actual(db: Session, token: str):
    # 1. decodificar el token
    payload = verificar_token(token)

    if not payload:
        raise ValueError("Token inválido o expirado")

    # 2. extraer el username del payload
    username = payload.get("sub")

    # 3. buscar el usuario en la BD
    usuario = db.query(Usuarios).filter(
        Usuarios.username == username
    ).first()

    if not usuario:
        raise ValueError("Usuario no encontrado")

    return usuario
