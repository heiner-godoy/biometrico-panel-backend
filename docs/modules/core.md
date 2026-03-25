# Módulo Core

## Descripción General

El directorio `core/` contiene las configuraciones centrales, utilidades de seguridad y dependencias compartidas de la aplicación. Este módulo proporciona la base técnica sobre la que se construye el resto del sistema.

## Estructura

```
core/
├── __init__.py        # Importaciones
├── config.py          # Configuraciones de aplicación
├── dependencies.py    # Dependencias FastAPI
└── security.py        # Utilidades de seguridad
```

## Config (`config.py`)

### Clase Settings
Configuración centralizada usando Pydantic Settings:

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 480
    TCP_HOST: str = "0.0.0.0"
    TCP_PORT: int = 7005
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:4200"
```

### Variables de Configuración

#### Base de Datos
- **DATABASE_URL**: Cadena de conexión PostgreSQL
- Formato: `postgresql://user:password@host:port/database`

#### JWT (JSON Web Tokens)
- **JWT_SECRET**: Clave secreta para firmar tokens
- **JWT_ALGORITHM**: Algoritmo de firma (HS256)
- **JWT_EXPIRE_MINUTES**: Expiración de tokens (480 min = 8 horas)

#### Red y Puertos
- **TCP_HOST/TCP_PORT**: Configuración del servidor TCP (7005)
- **API_HOST/API_PORT**: Configuración del servidor FastAPI (8000)

#### CORS
- **CORS_ORIGINS**: Orígenes permitidos separados por coma
- Propiedad `cors_list`: Lista parseada de orígenes

### Archivo de Entorno
- **.env**: Archivo para variables de entorno
- Carga automática con `BaseSettings`

## Security (`security.py`)

### Hashing de Contraseñas
```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

- **Bcrypt**: Algoritmo seguro para hashing
- **Async Verification**: `verify_password_async()` para no bloquear el event loop

### Gestión de JWT

#### crear_token()
- **Parámetros**: Diccionario con claims (sub, rol, id)
- **Expiración**: Calculada desde configuración
- **Retorno**: Token JWT firmado

#### verificar_token()
- **Parámetros**: Token JWT string
- **Validaciones**: Firma y expiración
- **Retorno**: Payload decodificado o None

### Claims del Token
```json
{
  "sub": "username",
  "rol": 1,
  "id": 123,
  "exp": 1640995200
}
```

## Dependencies (`dependencies.py`)

### Gestión de Base de Datos

#### get_db()
- **Propósito**: Proporcionar sesión SQLAlchemy
- **Tipo**: Generator (yield)
- **Cleanup**: Cierra sesión automáticamente
- **Uso**: `db: Session = Depends(get_db)`

### Autenticación y Autorización

#### oauth2_scheme
- **OAuth2PasswordBearer**: Esquema para extracción de tokens
- **tokenUrl**: Endpoint de login (`/api/auth/login`)

#### get_usuario_actual()
- **Propósito**: Obtener usuario desde token JWT
- **Validaciones**:
  - Token válido y no expirado
  - Usuario existe en BD
  - Usuario activo
- **Retorno**: Objeto `Usuarios` completo
- **Excepciones**: 401/404 según el caso

### Dependencias Adicionales
En otros archivos se definen dependencias como:
- `get_current_admin()`: Verificar rol de administrador
- `get_current_user_optional()`: Usuario opcional

## Integración con FastAPI

### Inyección de Dependencias
```python
@router.get("/protected")
def endpoint_protegido(
    usuario: Usuarios = Depends(get_usuario_actual),
    db: Session = Depends(get_db)
):
    # usuario y db disponibles
```

### Middleware
- **CORS**: Configurado con `settings.cors_list`
- **Autenticación**: Automática en rutas protegidas

## Seguridad Implementada

### Protección de Contraseñas
- **Hashing Irreversible**: Bcrypt con salt automático
- **Verificación Asíncrona**: No bloquea el servidor
- **Migración**: Soporte para algoritmos deprecated

### Tokens JWT
- **Firma HMAC**: HS256 con clave secreta
- **Expiración**: Configurable (8 horas por defecto)
- **Claims**: Información mínima necesaria
- **Stateless**: No requiere almacenamiento servidor

### Autorización
- **Role-Based Access Control**: Verificación de roles
- **Endpoint Protection**: Dependencias por ruta
- **Hierarchical Permissions**: Admin > User

## Configuración de Entorno

### Variables Requeridas
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/db
JWT_SECRET=your-super-secret-key-here
```

### Variables Opcionales
```bash
JWT_EXPIRE_MINUTES=480
TCP_PORT=7005
API_PORT=8000
CORS_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
```

## Consideraciones de Producción

- **Secrets Management**: JWT_SECRET debe ser fuerte y rotada
- **Environment Isolation**: Variables diferentes por entorno
- **CORS Security**: Solo orígenes confiables
- **Token Expiration**: Balance entre UX y seguridad

## Testing

Las utilidades de core son testeables:
- **Mock Settings**: Para configuración de pruebas
- **Test Tokens**: Generación de tokens de prueba
- **Database Isolation**: Sesiones de prueba independientes