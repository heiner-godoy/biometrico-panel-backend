# Módulo Schemas

## Descripción General

El directorio `schemas/` contiene las definiciones Pydantic para validación de datos en la API. Cada entidad tiene esquemas para crear, actualizar y responder, asegurando consistencia y validación automática.

## Estructura

```
schemas/
├── __init__.py     # Exportaciones de schemas
├── empleado.py     # Schemas para empleados
├── registro.py     # Schemas para registros
├── rol.py          # Schemas para roles
└── usuario.py      # Schemas para usuarios
```

## Patrón de Diseño

### Estructura por Entidad
Cada archivo define tres tipos de schemas:

```python
class CreateEntidad(BaseModel):
    # Campos requeridos para creación
    campo: Tipo = Field(..., description="Descripción")

class ResponseEntidad(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # Todos los campos para respuesta

class UpdateEntidad(BaseModel):
    # Campos opcionales para actualización
    campo: Optional[Tipo] = None
```

### Características Comunes
- **Field**: Validaciones y descripciones
- **Optional**: Campos no requeridos
- **ConfigDict**: Configuración Pydantic
- **from_attributes**: Conversión desde SQLAlchemy

## Schema Empleado (`empleado.py`)

### CreateEmpleado
Campos para crear un nuevo empleado:
- `bio_id`: ID biométrico (requerido, único)
- `nombre`: Nombre completo (requerido)
- `cedula`: Número de cédula (requerido, único)
- `cargo`: Posición laboral (opcional)
- `area`: Departamento (opcional)
- `tarjeta_rfid`: Código RFID (opcional, único)
- `tiene_huella`: Boolean para huella registrada
- `tiene_password`: Boolean para contraseña
- `permite_huella`: Permiso para usar huella
- `permite_rfid`: Permiso para usar RFID
- `permite_password`: Permiso para usar contraseña
- `activo`: Estado del empleado

### ResponseEmpleado
Incluye todos los campos del modelo más:
- `id_empleado`: ID autoincremental
- `creado_en`: Timestamp de creación

### UpdateEmpleado
Todos los campos como opcionales para actualizaciones parciales.

## Schema Registro (`registro.py`)

### CreateRegistro
Campos para crear registros manuales:
- `empleado_id`: ID del empleado
- `metodo`: Método de acceso (enum)
- `tipo`: Entrada/salida (enum)
- `fecha_hora`: Timestamp (opcional)
- `autorizado`: Boolean
- `motivo_bloqueo`: Razón del bloqueo

### ResponseRegistro
Incluye campos del modelo y relación con empleado.

### Filtros y Estadísticas
- `RegistroFilters`: Parámetros de consulta
- `EstadisticasResponse`: Conteos y métricas

## Schema Usuario (`usuario.py`)

### CreateUsuario
Campos para registro de usuarios:
- `username`: Nombre de usuario (requerido)
- `email`: Correo electrónico (requerido)
- `password`: Contraseña (requerido)
- `id_rol`: Rol asignado (requerido)

### ResponseUser
Campos públicos del usuario (sin password).

### UpdateUsuario
Campos actualizables (username, email, rol).

### Auth Schemas
- `Token`: Respuesta de login con JWT
- `TokenData`: Datos del token decodificado

## Schema Rol (`rol.py`)

### CreateRol
- `nombre`: Nombre del rol (requerido, único)

### ResponseRol
- `id_rol`: ID del rol
- `nombre`: Nombre del rol

## Validaciones Implementadas

### Validaciones de Campo
- **Longitudes máximas**: Evita overflow de BD
- **Formatos**: Email, cédula, etc.
- **Unicidad**: Verificada en BD
- **Enums**: Valores permitidos estrictos

### Validaciones de Negocio
- **Dependencias**: Campos relacionados
- **Estados**: Transiciones válidas
- **Permisos**: Verificación de autorización

## Configuración Pydantic

### ConfigDict
```python
model_config = ConfigDict(from_attributes=True)
```
- `from_attributes`: Convierte objetos SQLAlchemy a Pydantic
- Habilita compatibilidad con ORM

### Field Definitions
```python
campo: str = Field(..., max_length=100, description="Descripción")
```
- `max_length`: Validación de longitud
- `description`: Documentación automática
- `default`: Valores por defecto

## Uso en Routers

### Request Validation
```python
@router.post("/", response_model=ResponseSchema)
def crear(data: CreateSchema, db: Session = Depends(get_db)):
    return create_entity(data, db)
```

### Response Serialization
```python
@router.get("/", response_model=List[ResponseSchema])
def listar(entities = Depends(get_entities)):
    return entities
```

## Beneficios

- **Type Safety**: Validación en tiempo de desarrollo
- **Documentación**: APIs auto-documentadas
- **Consistencia**: Formatos uniformes
- **Seguridad**: Prevención de datos maliciosos
- **Mantenibilidad**: Cambios centralizados

## Consideraciones

- **Versionado**: Schemas pueden versionarse para compatibilidad
- **Herencia**: Base schemas para campos comunes
- **Validadores**: Lógica personalizada con `@field_validator`
- **Serialización**: Control de qué campos se exponen