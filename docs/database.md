# Esquema de Base de Datos

## Descripción General

El sistema utiliza PostgreSQL como base de datos relacional principal. El esquema está diseñado para almacenar información de empleados, registros de acceso, usuarios del sistema y roles de autorización. Utiliza SQLAlchemy como ORM para la gestión de datos.

## Diagrama Entidad-Relación

```
┌─────────────┐       ┌─────────────┐
│   Usuarios  │       │     Rol    │
├─────────────┤       ├─────────────┤
│ id_usuario  │       │ id_rol     │
│ id_rol ─────┼──────►│ nombre     │
│ username    │       └─────────────┘
│ email       │
│ password    │
│ activo      │
│ creado_en   │
│ ultimo_login│
└─────────────┘
       │
       │
       ▼
┌─────────────┐       ┌─────────────┐
│  Empleados  │       │  Registros  │
├─────────────┤       ├─────────────┤
│ id_empleado │       │ id_registro │
│ bio_id      │◄──────┤ empleado_id │
│ nombre      │       │ dispositivo_sn│
│ cedula      │       │ metodo      │
│ cargo       │       │ tipo        │
│ area        │       │ fecha_hora  │
│ tarjeta_rfid│       │ autorizado  │
│ tiene_huella│       │ motivo_bloqueo│
│ tiene_password│     │ creado_en   │
│ permite_huella│     └─────────────┘
│ permite_rfid │
│ permite_password│
│ activo      │
│ creado_en   │
└─────────────┘
```

## Tablas Detalladas

### Tabla `rol`

Almacena los diferentes roles de usuario en el sistema.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id_rol | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Identificador único del rol |
| nombre | VARCHAR(20) | NOT NULL, UNIQUE | Nombre del rol (ej: 'admin', 'visor') |

### Tabla `usuarios`

Gestiona los usuarios del sistema para autenticación y autorización.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id_usuario | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Identificador único del usuario |
| id_rol | INTEGER | FOREIGN KEY → rol.id_rol, NOT NULL | Rol asignado al usuario |
| username | VARCHAR(20) | NOT NULL, UNIQUE | Nombre de usuario para login |
| email | VARCHAR(100) | NOT NULL, UNIQUE, INDEX | Correo electrónico del usuario |
| password | VARCHAR(255) | NOT NULL | Contraseña encriptada |
| activo | BOOLEAN | NOT NULL, DEFAULT TRUE | Estado del usuario |
| creado_en | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| ultimo_login | TIMESTAMP | NULL | Última sesión del usuario |

### Tabla `empleados`

Contiene la información de los empleados registrados en el sistema biométrico.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id_empleado | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Identificador único del empleado |
| bio_id | VARCHAR(20) | NOT NULL, UNIQUE | ID biométrico del empleado |
| nombre | VARCHAR(255) | NOT NULL | Nombre completo del empleado |
| cedula | VARCHAR(20) | NOT NULL, UNIQUE | Número de cédula |
| cargo | VARCHAR(50) | NULL | Cargo o posición del empleado |
| area | VARCHAR(50) | NULL | Área o departamento |
| tarjeta_rfid | VARCHAR(100) | UNIQUE | Código de tarjeta RFID |
| tiene_huella | BOOLEAN | NOT NULL, DEFAULT FALSE | Si tiene huella registrada |
| tiene_password | BOOLEAN | NOT NULL, DEFAULT FALSE | Si tiene contraseña registrada |
| permite_huella | BOOLEAN | NOT NULL, DEFAULT TRUE | Permite acceso por huella |
| permite_rfid | BOOLEAN | NOT NULL, DEFAULT TRUE | Permite acceso por RFID |
| permite_password | BOOLEAN | NOT NULL, DEFAULT TRUE | Permite acceso por contraseña |
| activo | BOOLEAN | NOT NULL, DEFAULT TRUE | Estado del empleado |
| creado_en | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

### Tabla `registros`

Almacena todos los registros de acceso del sistema biométrico.

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id_registro | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Identificador único del registro |
| empleado_id | VARCHAR(20) | FOREIGN KEY → empleados.bio_id | ID del empleado (puede ser NULL) |
| dispositivo_sn | VARCHAR(50) | NULL | Número de serie del dispositivo |
| metodo | ENUM | NOT NULL | Método de acceso utilizado |
| tipo | ENUM | NOT NULL | Tipo de acceso (entrada/salida) |
| fecha_hora | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Fecha y hora del registro |
| autorizado | BOOLEAN | NOT NULL, DEFAULT TRUE | Si el acceso fue autorizado |
| motivo_bloqueo | VARCHAR(255) | NULL | Razón si fue bloqueado |
| creado_en | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Fecha de creación del registro |

## Enumeraciones

### MetodoAcceso

```sql
CREATE TYPE metodo_acceso AS ENUM (
    'huella',
    'password',
    'rfid',
    'huella_password',
    'huella_rfid',
    'desconocido'
);
```

### TipoAcceso

```sql
CREATE TYPE tipo_acceso AS ENUM (
    'entrada',
    'salida'
);
```

## Relaciones

- **usuarios → rol**: Muchos a uno (un rol puede tener múltiples usuarios)
- **registros → empleados**: Muchos a uno (un empleado puede tener múltiples registros)
- **empleados → registros**: Uno a muchos (relación bidireccional)

## Índices

- `usuarios.email` - Para búsquedas rápidas por email
- `empleados.bio_id` - Para búsquedas por ID biométrico
- `empleados.cedula` - Para validación de cédulas únicas
- `registros.fecha_hora` - Para consultas temporales
- `registros.empleado_id` - Para filtrado por empleado

## Configuración de Conexión

La conexión a la base de datos se configura mediante variables de entorno:

```python
DATABASE_URL = "postgresql://user:password@localhost:5432/biometrico_db"
```

Características de la conexión:
- **Pool de conexiones**: Gestión automática de conexiones
- **Pre-ping**: Reconexión automática si la BD se reinicia
- **Autocommit**: Deshabilitado para control transaccional
- **Autoflush**: Deshabilitado para control manual

## Migraciones

El sistema utiliza SQLAlchemy con `metadata.create_all()` para crear las tablas automáticamente al iniciar la aplicación. En producción, se recomienda usar herramientas como Alembic para migraciones controladas.

## Consideraciones de Rendimiento

- **Particionamiento**: La tabla `registros` puede requerir particionamiento por fecha en sistemas de alto volumen
- **Índices compuestos**: Considerar índices en `(empleado_id, fecha_hora)` para reportes
- **Archivado**: Implementar estrategias de archivado para registros históricos