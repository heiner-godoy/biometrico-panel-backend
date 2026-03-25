# Arquitectura del Sistema Biométrico

## Visión General

El sistema biométrico panel está diseñado siguiendo una arquitectura modular y escalable, separando claramente las responsabilidades entre diferentes capas y componentes. Utiliza FastAPI como framework principal para el backend, PostgreSQL como base de datos relacional, y comunicación TCP directa con el dispositivo biométrico VTA-70075.

## Diagrama de Arquitectura

```
┌─────────────────┐    TCP/IP     ┌─────────────────────┐
│ Dispositivo     │──────────────►│ Servidor TCP        │
│ Biométrico      │   Puerto 7005 │ (tcp_server.py)    │
│ VTA-70075       │               └─────────────────────┘
└─────────────────┘                       │
                                          │
                                          ▼
┌─────────────────┐    WebSocket   ┌─────────────────────┐
│ Cliente Web     │◄──────────────►│ WebSocket Manager   │
│ (Frontend)      │                │ (websocket_manager.py)
└─────────────────┘                └─────────────────────┘
                                          │
                                          ▼
┌─────────────────┐    HTTP/REST   ┌─────────────────────┐
│ Cliente API     │◄──────────────►│ FastAPI Application │
│                 │                │ (main.py)           │
└─────────────────┘                └─────────────────────┘
                                          │
                                          ▼
┌─────────────────┐    SQLAlchemy  ┌─────────────────────┐
│ Base de Datos   │◄──────────────►│ Database Layer      │
│ PostgreSQL      │                │ (database.py)       │
└─────────────────┘                └─────────────────────┘
```

## Componentes Principales

### 1. Servidor TCP (`tcp_server.py`)

**Responsabilidades:**
- Escuchar conexiones entrantes del dispositivo biométrico en el puerto 7005
- Parsear paquetes de datos binarios enviados por el dispositivo
- Extraer información de registros (ID empleado, timestamp, tipo de acceso, método)
- Almacenar registros en la base de datos
- Gestionar conexiones múltiples de dispositivos

**Protocolo de Comunicación:**
- Puerto: 7005
- Formato: Binario con estructura fija
- Campos: user_id (4 bytes), timestamp (4 bytes), tipo_acceso (1 byte), metodo (1 byte)

### 2. Aplicación FastAPI (`main.py`)

**Responsabilidades:**
- Servir la API REST para gestión del sistema
- Gestionar el ciclo de vida de la aplicación (lifespan)
- Configurar CORS para comunicación con frontend
- Inicializar base de datos y servidor TCP al inicio
- Proporcionar documentación automática de API

**Características:**
- Versionado de API (v1.0.0)
- Middleware CORS configurado
- Gestión de tareas asíncronas (TCP server)

### 3. Gestor WebSocket (`websocket_manager.py`)

**Responsabilidades:**
- Gestionar conexiones WebSocket para actualizaciones en tiempo real
- Broadcast de nuevos registros a clientes conectados
- Manejo de eventos de conexión/desconexión
- Filtrado de mensajes por permisos de usuario

### 4. Capa de Base de Datos (`database.py`)

**Responsabilidades:**
- Configuración de conexión a PostgreSQL
- Gestión de sesiones de base de datos
- Creación automática de tablas
- Pool de conexiones con reconexión automática

**Configuración:**
- Engine SQLAlchemy con pool_pre_ping=True
- SessionLocal para gestión de transacciones
- Base declarativa para modelos

## Arquitectura por Capas

### Capa de Presentación
- **Routers**: Endpoints REST (`routers/`)
- **Schemas**: Validación de datos con Pydantic (`schemas/`)
- **WebSockets**: Comunicación en tiempo real

### Capa de Lógica de Negocio
- **Controllers**: Lógica de aplicación (`controllers/`)
- **Services**: Servicios de negocio (`services/`)

### Capa de Datos
- **Models**: Definición de entidades (`models/`)
- **Database**: Conexión y configuración BD

### Capa Central
- **Core**: Configuraciones, seguridad, dependencias (`core/`)

## Flujo de Datos

1. **Registro Biométrico**:
   - Dispositivo → TCP Server → Parsing → Database → WebSocket Broadcast

2. **Consulta API**:
   - Cliente → Router → Controller/Service → Model → Database → Response

3. **Autenticación**:
   - Cliente → Auth Router → Security Service → JWT Token

## Seguridad

- **Autenticación JWT**: Tokens con expiración
- **Roles y Permisos**: Admin/Visor con diferentes niveles de acceso
- **Validación de Datos**: Pydantic schemas en todas las entradas
- **CORS**: Configurado para orígenes específicos
- **Encriptación**: Claves y datos sensibles protegidos

## Escalabilidad

- **Asincronía**: Uso de async/await en operaciones I/O
- **Pool de Conexiones**: Gestión eficiente de conexiones BD
- **WebSockets**: Comunicación eficiente para múltiples clientes
- **Modularidad**: Separación clara de responsabilidades

## Despliegue

- **Contenedor**: Docker para aislamiento
- **Variables de Entorno**: Configuración externa
- **Logging**: Registro de eventos del sistema
- **Monitoreo**: Health checks y métricas