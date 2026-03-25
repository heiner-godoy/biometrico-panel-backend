# Módulo Backend

## Descripción General

El directorio `backend/` contiene todo el código del servidor de la aplicación. Está estructurado siguiendo el patrón de arquitectura limpia (Clean Architecture) con separación clara de responsabilidades.

## Estructura de Archivos

```
backend/
├── main.py              # Punto de entrada de FastAPI
├── database.py          # Configuración de base de datos
├── tcp_server.py       # Servidor TCP para dispositivo biométrico
├── websocket_manager.py # Gestión de WebSockets
├── usuarioadmin.py      # Usuario administrador por defecto
├── clave.py             # Utilidades de encriptación
├── controllers/         # Lógica de negocio
├── core/                # Configuraciones centrales
├── models/              # Modelos de datos SQLAlchemy
├── routers/             # Endpoints REST API
├── schemas/             # Validación Pydantic
└── services/            # Servicios de aplicación
```

## Archivos Principales

### main.py

**Propósito**: Punto de entrada principal de la aplicación FastAPI.

**Funcionalidades**:
- Configuración de la aplicación FastAPI
- Gestión del ciclo de vida (lifespan)
- Configuración de CORS
- Inicialización de base de datos
- Inicio del servidor TCP
- Registro de routers de la API

**Dependencias**:
- FastAPI para el framework web
- SQLAlchemy para ORM
- asyncio para operaciones asíncronas

**Configuración CORS**:
```python
allow_origins = ["http://localhost:4200", "http://127.0.0.1:4200"]
```

### database.py

**Propósito**: Configuración y gestión de la conexión a PostgreSQL.

**Funcionalidades**:
- Creación del engine SQLAlchemy
- Configuración del pool de conexiones
- Gestión de sesiones de base de datos
- Creación automática de tablas
- Reconexión automática (pool_pre_ping)

**Configuración**:
- Engine con pool_pre_ping=True
- SessionLocal para transacciones
- Base declarativa para modelos

### tcp_server.py

**Propósito**: Servidor TCP para comunicación con el dispositivo biométrico VTA-70075.

**Funcionalidades**:
- Escucha en puerto 7005
- Parsing de paquetes binarios
- Extracción de datos de registros
- Almacenamiento en base de datos
- Manejo de múltiples conexiones

**Protocolo**:
- Puerto: 7005
- Formato binario con campos fijos
- Campos: user_id, timestamp, tipo_acceso, metodo

### websocket_manager.py

**Propósito**: Gestión de conexiones WebSocket para actualizaciones en tiempo real.

**Funcionalidades**:
- Conexiones WebSocket activas
- Broadcast de nuevos registros
- Gestión de eventos de conexión/desconexión
- Filtrado por permisos de usuario

### usuarioadmin.py

**Propósito**: Creación del usuario administrador por defecto.

**Funcionalidades**:
- Verificación de existencia de admin
- Creación automática si no existe
- Configuración inicial del sistema

### clave.py

**Propósito**: Utilidades para encriptación y manejo de claves.

**Funcionalidades**:
- Generación de hashes de contraseña
- Verificación de contraseñas
- Algoritmos de encriptación seguros

## Submódulos

### controllers/
Contiene la lógica de negocio de la aplicación. Cada entidad tiene su propio controlador que maneja las operaciones CRUD y la lógica específica.

### core/
Configuraciones centrales del sistema:
- `config.py`: Variables de entorno y configuraciones
- `dependencies.py`: Dependencias inyectables
- `security.py`: Utilidades de seguridad y JWT

### models/
Modelos de datos SQLAlchemy que representan las tablas de la base de datos.

### routers/
Endpoints REST de la API FastAPI, organizados por entidad.

### schemas/
Esquemas Pydantic para validación de entrada/salida de datos.

### services/
Servicios de negocio que encapsulan lógica compleja y operaciones con la base de datos.

## Configuración y Variables de Entorno

El sistema utiliza variables de entorno para configuración:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/biometrico_db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
```

## Inicialización

Al iniciar la aplicación:

1. Se crea la conexión a la base de datos
2. Se crean las tablas si no existen
3. Se inicia el servidor TCP en background
4. Se registra el usuario admin si no existe
5. FastAPI comienza a servir la API

## Manejo de Errores

- Excepciones de base de datos se manejan con rollback automático
- Errores de TCP se registran pero no detienen el servidor
- Validaciones de Pydantic en todas las entradas
- Logging configurado para debugging

## Pruebas

El directorio `test/` contiene pruebas unitarias e integración:
- `test_db.py`: Pruebas de conexión a base de datos
- `test_tablas.py`: Validación de creación de tablas