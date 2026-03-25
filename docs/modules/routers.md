# Módulo Routers

## Descripción General

El directorio `routers/` contiene los endpoints REST de la API FastAPI. Cada archivo define las rutas para una entidad específica del sistema, siguiendo el patrón RESTful.

## Estructura

```
routers/
├── __init__.py      # Importaciones de routers
├── auth.py          # Endpoints de autenticación
├── empleado.py      # CRUD de empleados
├── registro.py      # Gestión de registros
├── rol.py           # Administración de roles
└── usuario.py       # Gestión de usuarios
```

## Patrón de Diseño

### Estructura Común
Cada router sigue el mismo patrón:

```python
from fastapi import APIRouter, Depends
from controllers.modulo import funciones_controller
from schemas.modulo import schemas_pydantic

router = APIRouter(prefix="/entidad", tags=["Etiqueta"])

@router.get("/", response_model=List[ResponseSchema])
def listar(resultado=Depends(funcion_controller)):
    return resultado
```

### Características
- **Prefix**: Ruta base para el módulo
- **Tags**: Etiquetas para documentación automática
- **Depends**: Inyección de dependencias para lógica de negocio
- **Response Models**: Validación de salida con Pydantic

## Router Auth (`auth.py`)

### Endpoints

#### POST `/auth/login`
- **Descripción**: Autenticación de usuario
- **Body**: `OAuth2PasswordRequestForm`
- **Respuesta**: Token JWT + información de usuario
- **Dependencias**: Base de datos

#### GET `/auth/me`
- **Descripción**: Información del usuario actual
- **Autenticación**: Requiere JWT
- **Respuesta**: `ResponseUser`
- **Dependencias**: Token válido

## Router Empleado (`empleado.py`)

### Endpoints CRUD

#### GET `/empleados/`
- **Descripción**: Listar todos los empleados
- **Respuesta**: `List[ResponseEmpleado]`
- **Filtros**: Activos por defecto

#### GET `/empleados/bio/{bio_id}`
- **Descripción**: Obtener empleado por ID biométrico
- **Parámetros**: `bio_id` (path)
- **Respuesta**: `ResponseEmpleado`

#### GET `/empleados/cedula/{cedula}`
- **Descripción**: Buscar empleado por cédula
- **Parámetros**: `cedula` (path)
- **Respuesta**: `ResponseEmpleado`

#### POST `/empleados/`
- **Descripción**: Crear nuevo empleado
- **Body**: Datos del empleado
- **Respuesta**: `ResponseEmpleado` (201)

#### PATCH `/empleados/{bio_id}`
- **Descripción**: Actualizar empleado
- **Parámetros**: `bio_id` (path)
- **Body**: Campos a actualizar
- **Respuesta**: `ResponseEmpleado`

#### DELETE `/empleados/{bio_id}`
- **Descripción**: Desactivar empleado
- **Parámetros**: `bio_id` (path)
- **Respuesta**: `ResponseEmpleado`

## Router Registro (`registro.py`)

### Endpoints

#### GET `/registros/`
- **Descripción**: Listar registros con filtros
- **Parámetros Query**:
  - `fecha_desde`: Fecha inicial
  - `fecha_hasta`: Fecha final
  - `empleado_id`: Filtrar por empleado
  - `tipo`: entrada/salida
  - `autorizado`: true/false
- **Paginación**: `skip`, `limit`

#### GET `/registros/{id_registro}`
- **Descripción**: Obtener registro específico
- **Parámetros**: `id_registro` (path)

#### POST `/registros/`
- **Descripción**: Crear registro manual
- **Uso**: Principalmente para pruebas

#### GET `/registros/estadisticas`
- **Descripción**: Estadísticas de acceso
- **Parámetros**: Rango de fechas
- **Respuesta**: Conteos por método, hora, día

#### GET `/registros/exportar`
- **Descripción**: Exportar registros a CSV
- **Parámetros**: Filtros de consulta
- **Respuesta**: Archivo CSV

## Router Rol (`rol.py`)

### Endpoints

#### GET `/roles/`
- **Descripción**: Listar roles disponibles
- **Respuesta**: `List[ResponseRol]`

#### POST `/roles/`
- **Descripción**: Crear nuevo rol
- **Body**: Datos del rol
- **Permisos**: Solo admin

## Router Usuario (`usuario.py`)

### Endpoints

#### GET `/usuarios/`
- **Descripción**: Listar usuarios
- **Permisos**: Admin o propio usuario

#### GET `/usuarios/{id_usuario}`
- **Descripción**: Obtener usuario específico

#### POST `/usuarios/`
- **Descripción**: Crear nuevo usuario
- **Body**: Datos de usuario
- **Permisos**: Admin

#### PATCH `/usuarios/{id_usuario}`
- **Descripción**: Actualizar usuario
- **Permisos**: Admin o propio usuario

#### DELETE `/usuarios/{id_usuario}`
- **Descripción**: Desactivar usuario
- **Permisos**: Admin

## Middleware y Dependencias

### Autenticación
- **JWT Required**: `Depends(get_current_user)`
- **Admin Only**: `Depends(get_current_admin)`
- **Optional**: `Depends(get_current_user_optional)`

### Base de Datos
- **Session**: `Depends(get_db)`
- Inyección automática de sesión SQLAlchemy

### Validación
- **Pydantic Models**: Validación automática de entrada/salida
- **Response Models**: Garantiza formato de respuesta

## Documentación Automática

FastAPI genera documentación automática en:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

Los routers están etiquetados para organización:
- `Auth`: Autenticación
- `Empleados`: Gestión de empleados
- `Registros`: Historial de accesos
- `Roles`: Administración de roles
- `Usuarios`: Gestión de usuarios

## Consideraciones de Seguridad

- **Autenticación**: JWT en headers Authorization
- **Autorización**: Verificación de roles por endpoint
- **Validación**: Pydantic previene datos maliciosos
- **Rate Limiting**: Implementado en controladores

## Manejo de Errores

- **HTTPException**: Errores específicos (404, 401, 403, etc.)
- **ValidationError**: Datos inválidos
- **DatabaseError**: Problemas de BD
- Respuestas consistentes con códigos apropiados