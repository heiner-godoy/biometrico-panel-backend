from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import verificar_token
from models.usuario import Usuarios

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuarios:
    
    # 1. verificar el token
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    # 2. extraer el username del payload
    username = payload.get("sub")
    
    # 3. buscar el usuario en la BD
    usuario = db.query(Usuarios).filter(
        Usuarios.username == username
    ).first()
    
    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo"
        )
    
    return usuario