from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. encriptar contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 2. verificar contraseña
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# 3. crear JWT
def crear_token(data: dict) -> str:
    payload = data.copy()
    expira = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )
    payload.update({"exp": expira})
    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

# 4. verificar y decodificar JWT
def verificar_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        return None