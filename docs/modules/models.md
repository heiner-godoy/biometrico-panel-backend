# Módulo Models

## Descripción General

El directorio `models/` contiene las definiciones de datos del sistema utilizando SQLAlchemy ORM. Cada archivo representa una entidad de la base de datos con sus campos, relaciones y métodos.

## Estructura

```
models/
├── __init__.py     # Importaciones de modelos
├── empleado.py     # Modelo Empleados
├── registro.py     # Modelo Registros
├── rol.py          # Modelo Rol
└── usuario.py      # Modelo Usuarios
```

## Modelo Empleados (`empleado.py`)

### Descripción
Representa a los empleados registrados en el sistema biométrico.

### Campos Principales
- `id_empleado`: Identificador único autoincremental
- `bio_id`: ID biométrico único (clave primaria para registros)
- `nombre`: Nombre completo del empleado
- `cedula`: Número de cédula (único)
- `cargo`: Posición laboral
- `area`: Departamento o área

### Métodos de Autenticación
- `tiene_huella`: Si tiene huella registrada en el dispositivo
- `tiene_password`: Si tiene contraseña registrada
- `permite_huella`: Permiso para usar huella
- `permite_rfid`: Permiso para usar tarjeta RFID
- `permite_password`: Permiso para usar contraseña

### Relaciones
- `registros`: Relación uno-a-muchos con la tabla Registros

### Consideraciones
- Los campos `permite_*` permiten bloquear métodos individualmente
- `tarjeta_rfid` puede ser NULL si no tiene tarjeta asignada
- `activo` controla si el empleado puede marcar asistencia

## Modelo Registros (`registro.py`)

### Descripción
Almacena todos los eventos de acceso del sistema biométrico.

### Enumeraciones
```python
class MetodoAcceso(str, enum.Enum):
    huella = "huella"
    password = "password"
    rfid = "rfid"
    huella_password = "huella_password"
    huella_rfid = "huella_rfid"
    desconocido = "desconocido"

class TipoAcceso(str, enum.Enum):
    entrada = "entrada"
    salida = "salida"
```

### Campos Principales
- `id_registro`: Identificador único
- `empleado_id`: Referencia al bio_id del empleado
- `dispositivo_sn`: Número de serie del dispositivo
- `metodo`: Método de acceso utilizado
- `tipo`: Entrada o salida
- `fecha_hora`: Timestamp del evento
- `autorizado`: Si el acceso fue autorizado
- `motivo_bloqueo`: Razón del bloqueo (si aplica)

### Relaciones
- `empleado`: Relación muchos-a-uno con Empleados

### Consideraciones
- `empleado_id` puede ser NULL para accesos no identificados
- `autorizado` se determina por permisos del empleado
- `motivo_bloqueo` explica por qué fue rechazado

## Modelo Rol (`rol.py`)

### Descripción
Define los roles de usuario para autorización.

### Campos
- `id_rol`: Identificador único
- `nombre`: Nombre del rol (ej: "admin", "visor")

### Relaciones
- `usuarios`: Relación uno-a-muchos con Usuarios

### Roles Predefinidos
- **Admin**: Acceso completo al sistema
- **Visor**: Solo lectura y reportes

## Modelo Usuarios (`usuario.py`)

### Descripción
Gestiona los usuarios del panel web para autenticación.

### Campos Principales
- `id_usuario`: Identificador único
- `id_rol`: Referencia al rol asignado
- `username`: Nombre de usuario para login
- `email`: Correo electrónico único
- `password`: Contraseña encriptada
- `activo`: Estado del usuario
- `creado_en`: Fecha de creación
- `ultimo_login`: Última sesión

### Relaciones
- `rol`: Relación muchos-a-uno con Rol

### Consideraciones
- Email indexado para búsquedas rápidas
- Password debe estar encriptada
- `ultimo_login` se actualiza en cada autenticación

## Configuración General

### Base Declarativa
Todos los modelos heredan de `Base` de SQLAlchemy:
```python
from database import Base

class MiModelo(Base):
    __tablename__ = "mi_tabla"
```

### Timestamps
Los campos de fecha usan timezone-aware datetimes:
```python
creado_en = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
```

### Relaciones Bidireccionales
Las relaciones se definen con `relationship` y `back_populates`:
```python
# En Empleados
registros = relationship("Registros", back_populates="empleado")

# En Registros
empleado = relationship("Empleados", back_populates="registros")
```

## Validaciones y Restricciones

### Constraints de Base de Datos
- Claves primarias autoincrementales
- Unicidad en campos críticos (cedula, bio_id, email, username)
- Foreign keys con integridad referencial
- Valores por defecto apropiados

### Validaciones de Aplicación
- Longitudes máximas de strings
- Formatos específicos (cedula, email)
- Valores booleanos con defaults

## Migraciones

Los modelos se crean automáticamente con:
```python
Base.metadata.create_all(bind=engine)
```

Para cambios en producción, considerar Alembic para migraciones versionadas.

## Consideraciones de Rendimiento

- Índices en campos de búsqueda frecuente
- Relaciones lazy loading por defecto
- Campos calculados donde sea necesario
- Particionamiento potencial para tablas grandes (registros)