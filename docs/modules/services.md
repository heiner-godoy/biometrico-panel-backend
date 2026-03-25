# Módulo Services

## Descripción General

El directorio `services/` contiene servicios de negocio que encapsulan lógica compleja y operaciones puras con la base de datos. Estos servicios son independientes del framework HTTP y pueden ser reutilizados en diferentes contextos.

## Estructura

```
services/
├── __init__.py        # Importaciones
├── auth_service.py    # Servicios de autenticación
├── empleado.py        # Servicios de empleados
├── registro.py        # Servicios de registros
├── rol.py             # Servicios de roles
└── usuario.py         # Servicios de usuarios
```

## Patrón de Diseño

### Servicios Puros
Los servicios implementan lógica de negocio pura:

```python
def servicio_operacion(
    db: Session,
    datos: InputType,
    usuario: Usuario = None
) -> OutputType:
    # Validaciones de negocio
    # Operaciones de BD
    # Cálculos y lógica
    # Retorno de resultado
```

### Características
- **Sin dependencias HTTP**: No manejan requests/responses
- **Transaccionales**: Operaciones atómicas
- **Reutilizables**: Llamables desde controllers, tests, etc.
- **Excepciones de negocio**: ValueError para errores lógicos

## Auth Service (`auth_service.py`)

### Funciones

#### login()
- **Propósito**: Autenticar credenciales y generar token
- **Parámetros**: `db`, `username`, `password`
- **Validaciones**:
  - Usuario existe
  - Contraseña correcta
  - Usuario activo
- **Retorno**: Diccionario con token JWT
- **Excepciones**: ValueError con mensaje descriptivo

#### get_usuario_actual()
- **Propósito**: Obtener usuario desde token
- **Parámetros**: `db`, `token`
- **Validaciones**:
  - Token válido
  - Usuario existe
- **Retorno**: Objeto Usuario
- **Excepciones**: ValueError para token inválido

### Beneficios
- **Separación de Concerns**: Lógica de auth independiente de HTTP
- **Testeable**: Fácil mocking de BD
- **Reutilizable**: Usable en diferentes endpoints

## Empleado Service (`empleado.py`)

### Operaciones CRUD

#### crear_empleado()
- **Propósito**: Crear nuevo empleado con validaciones
- **Validaciones**:
  - Unicidad de bio_id y cédula
  - Datos requeridos presentes
- **Retorno**: Empleado creado

#### actualizar_empleado()
- **Propósito**: Actualizar datos del empleado
- **Validaciones**:
  - Empleado existe
  - Unicidad de campos únicos
  - Transiciones de estado válidas
- **Retorno**: Empleado actualizado

#### buscar_empleado()
- **Propósito**: Búsqueda flexible de empleados
- **Parámetros**: Filtros (nombre, cédula, bio_id, etc.)
- **Retorno**: Lista de empleados matching

### Lógica de Negocio
- **Métodos de Acceso**: Gestión de permisos por empleado
- **Estados**: Control de empleados activos/inactivos
- **Relaciones**: Mantenimiento de integridad referencial

## Registro Service (`registro.py`)

### Gestión de Registros

#### crear_registro()
- **Propósito**: Registrar nuevo acceso
- **Validaciones**:
  - Empleado existe y está activo
  - Método permitido para el empleado
  - Datos temporales válidos
- **Lógica**: Determinación automática de autorización

#### consultar_registros()
- **Propósito**: Consulta avanzada con filtros
- **Parámetros**: Filtros complejos (fecha, empleado, método, etc.)
- **Paginación**: Soporte para listas grandes
- **Retorno**: Registros con metadata

#### calcular_estadisticas()
- **Propósito**: Análisis de datos de acceso
- **Cálculos**:
  - Conteo por método de acceso
  - Distribución por horas del día
  - Tendencias por días
- **Retorno**: Objeto con métricas agregadas

#### exportar_datos()
- **Propósito**: Generar reportes en diferentes formatos
- **Formatos**: CSV, JSON, etc.
- **Filtros**: Aplicación de criterios de consulta
- **Retorno**: Datos serializados

### Inteligencia de Negocio
- **Detección de Anomalías**: Patrones inusuales de acceso
- **Autorización Automática**: Basada en permisos del empleado
- **Bloqueo Inteligente**: Motivos específicos de denegación

## Usuario Service (`usuario.py`)

### Gestión de Usuarios

#### gestionar_usuario()
- **Propósito**: Operaciones completas de usuario
- **Funciones**:
  - Creación con encriptación de password
  - Actualización con validaciones
  - Desactivación segura
  - Cambio de roles

#### validar_credenciales()
- **Propósito**: Verificación de login
- **Validaciones**:
  - Usuario existe y activo
  - Password correcto
  - Cuenta no bloqueada

### Seguridad
- **Encriptación**: Passwords hasheados
- **Auditoría**: Registro de cambios
- **Políticas**: Reglas de complejidad de password

## Rol Service (`rol.py`)

### Administración de Roles

#### gestionar_roles()
- **Propósito**: CRUD de roles del sistema
- **Validaciones**:
  - Nombres únicos
  - Roles no eliminables si en uso
- **Permisos**: Solo administradores

#### verificar_permisos()
- **Propósito**: Control de acceso basado en roles
- **Parámetros**: Usuario, recurso, acción
- **Retorno**: Boolean de autorización

## Arquitectura de Servicios

### Separación de Responsabilidades
- **Controllers**: Manejo HTTP, serialización
- **Services**: Lógica de negocio, validaciones
- **Models**: Definición de datos
- **Schemas**: Validación de entrada/salida

### Ventajas
- **Testabilidad**: Servicios testeables sin HTTP
- **Reutilización**: Lógica usable en diferentes contextos
- **Mantenibilidad**: Cambios localizados
- **Performance**: Operaciones optimizadas

## Manejo de Transacciones

### Patrones Transaccionales
```python
def operacion_compleja(db: Session, datos):
    try:
        # Múltiples operaciones
        paso1 = servicio1(db, datos)
        paso2 = servicio2(db, paso1)
        db.commit()
        return paso2
    except Exception as e:
        db.rollback()
        raise
```

### Isolation Levels
- **Read Committed**: Nivel por defecto
- **Serializable**: Para operaciones críticas
- **Control Manual**: Commit/rollback explícito

## Validaciones de Negocio

### Tipos de Validación
- **Existencia**: Recursos referenciados existen
- **Permisos**: Usuario autorizado para la operación
- **Estado**: Transiciones válidas
- **Integridad**: Constraints de negocio

### Estrategias
- **Fail Fast**: Validar temprano
- **Consistencia**: Validaciones en todos los paths
- **Mensajes Claros**: Errores descriptivos

## Optimizaciones

### Queries Eficientes
- **Joins Apropiados**: Evitar N+1 queries
- **Índices**: Uso de índices de BD
- **Paginación**: Para resultados grandes
- **Caching**: Para datos frecuentemente accedidos

### Performance
- **Lazy Loading**: Carga diferida de relaciones
- **Batch Operations**: Operaciones masivas
- **Query Optimization**: Análisis y mejora de queries

## Testing

Los servicios están diseñados para testing:
- **Mock Database**: Sesiones de prueba
- **Datos de Test**: Fixtures consistentes
- **Aserciones**: Validación de lógica de negocio
- **Cobertura**: Tests unitarios completos