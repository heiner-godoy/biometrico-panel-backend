# Módulo Controllers

## Descripción General

El directorio `controllers/` contiene la lógica de negocio de la aplicación. Cada archivo implementa las operaciones CRUD y reglas de negocio para una entidad específica, separando la lógica de los endpoints REST.

## Estructura

```
controllers/
├── __init__.py     # Importaciones
├── auth.py         # Lógica de autenticación
├── empleado.py     # Gestión de empleados
├── registro.py     # Manejo de registros
├── rol.py          # Administración de roles
└── usuario.py      # Gestión de usuarios
```

## Patrón de Diseño

### Estructura de Funciones
Cada controller define funciones puras que:

```python
def operacion_entidad(
    datos: SchemaInput,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
) -> SchemaOutput:
    # Validaciones
    # Lógica de negocio
    # Operaciones BD
    # Retorno de resultado
```

### Características
- **Dependencias**: Inyección de DB y usuario
- **Validación**: Verificación de permisos y datos
- **Transacciones**: Manejo de sesiones SQLAlchemy
- **Excepciones**: HTTPException para errores

## Controller Auth (`auth.py`)

### Funciones

#### login()
- **Propósito**: Autenticar usuario y generar JWT
- **Parámetros**: `OAuth2PasswordRequestForm`, `Session`
- **Validaciones**:
  - Usuario existe
  - Contraseña correcta (verificación asíncrona)
  - Usuario activo
- **Retorno**: Token JWT + metadata

#### me()
- **Propósito**: Obtener datos del usuario actual
- **Parámetros**: Usuario actual (de token)
- **Retorno**: `ResponseUser` sin contraseña

### Seguridad
- **Hashing**: Contraseñas verificadas de forma asíncrona
- **JWT**: Tokens con claims (username, rol, id)
- **Estados**: Solo usuarios activos pueden loguear

## Controller Empleado (`empleado.py`)

### Operaciones CRUD

#### get_empleados()
- **Propósito**: Listar empleados activos
- **Filtros**: Solo empleados activos por defecto
- **Retorno**: Lista de empleados

#### get_empleado_by_id()
- **Propósito**: Buscar por ID biométrico
- **Validaciones**: Empleado existe
- **Retorno**: Empleado específico

#### get_empleado_by_cedula()
- **Propósito**: Buscar por número de cédula
- **Validaciones**: Cédula existe
- **Retorno**: Empleado encontrado

#### create_empleado()
- **Propósito**: Crear nuevo empleado
- **Validaciones**:
  - Bio_id único
  - Cédula única
  - Datos requeridos presentes
- **Retorno**: Empleado creado

#### update_empleado()
- **Propósito**: Actualizar datos del empleado
- **Validaciones**:
  - Empleado existe
  - Unicidad de campos únicos
  - Permisos de usuario
- **Retorno**: Empleado actualizado

#### delete_empleado()
- **Propósito**: Desactivar empleado (soft delete)
- **Validaciones**: Empleado existe
- **Retorno**: Empleado desactivado

## Controller Registro (`registro.py`)

### Funciones Principales

#### get_registros()
- **Propósito**: Listar registros con filtros
- **Parámetros**: Filtros de fecha, empleado, tipo, etc.
- **Paginación**: skip/limit
- **Retorno**: Lista paginada de registros

#### get_registro_by_id()
- **Propósito**: Obtener registro específico
- **Validaciones**: Registro existe
- **Retorno**: Registro detallado

#### create_registro()
- **Propósito**: Crear registro manual
- **Validaciones**: Empleado existe, datos válidos
- **Retorno**: Registro creado

#### get_estadisticas()
- **Propósito**: Calcular estadísticas de acceso
- **Parámetros**: Rango de fechas
- **Cálculos**:
  - Conteo por método
  - Conteo por hora
  - Conteo por día
- **Retorno**: Objeto con métricas

#### exportar_csv()
- **Propósito**: Generar archivo CSV de registros
- **Parámetros**: Filtros de consulta
- **Formato**: CSV con headers apropiados
- **Retorno**: StreamingResponse con archivo

## Controller Usuario (`usuario.py`)

### Gestión de Usuarios

#### get_usuarios()
- **Propósito**: Listar usuarios del sistema
- **Permisos**: Admin o usuario propio
- **Retorno**: Lista de usuarios (sin passwords)

#### get_usuario_by_id()
- **Propósito**: Obtener usuario específico
- **Validaciones**: Usuario existe, permisos adecuados
- **Retorno**: Datos del usuario

#### create_usuario()
- **Propósito**: Crear nuevo usuario
- **Validaciones**:
  - Username único
  - Email único
  - Rol válido
  - Password segura
- **Encriptación**: Password hasheada
- **Retorno**: Usuario creado

#### update_usuario()
- **Propósito**: Actualizar datos de usuario
- **Validaciones**: Permisos (admin o propio usuario)
- **Retorno**: Usuario actualizado

#### delete_usuario()
- **Propósito**: Desactivar usuario
- **Permisos**: Solo admin
- **Validaciones**: No puede eliminarse a sí mismo
- **Retorno**: Usuario desactivado

## Controller Rol (`rol.py`)

### Administración de Roles

#### get_roles()
- **Propósito**: Listar roles disponibles
- **Retorno**: Lista de roles

#### create_rol()
- **Propósito**: Crear nuevo rol
- **Validaciones**: Nombre único
- **Permisos**: Solo admin
- **Retorno**: Rol creado

## Manejo de Errores

### Excepciones Comunes
- **404 Not Found**: Recurso no existe
- **401 Unauthorized**: Credenciales inválidas
- **403 Forbidden**: Permisos insuficientes
- **400 Bad Request**: Datos inválidos
- **409 Conflict**: Violación de unicidad

### Patrones de Error
```python
if not entity:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Entidad no encontrada"
    )
```

## Transacciones y Concurrencia

- **Sesiones**: Cada operación usa su propia sesión
- **Commits**: Automáticos en operaciones exitosas
- **Rollbacks**: Automáticos en excepciones
- **Isolation**: Nivel por defecto de PostgreSQL

## Validaciones de Negocio

- **Unicidad**: Verificación de campos únicos
- **Permisos**: Control de acceso basado en roles
- **Estados**: Transiciones válidas (activo/inactivo)
- **Relaciones**: Integridad referencial

## Optimizaciones

- **Queries**: Optimizadas con joins apropiados
- **Filtros**: Aplicados en BD cuando posible
- **Paginación**: Para listas grandes
- **Índices**: Uso de índices de BD

## Testing

Los controllers están diseñados para ser testeables:
- **Dependencias inyectadas**: Fácil mocking
- **Funciones puras**: Lógica aislada
- **Excepciones claras**: Fácil verificación de errores