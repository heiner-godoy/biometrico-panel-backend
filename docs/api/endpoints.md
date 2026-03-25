# Documentación de la API

## Descripción General

La API REST del sistema biométrico está construida con FastAPI y proporciona endpoints para gestión completa del sistema de control de acceso. Incluye autenticación JWT, operaciones CRUD y funcionalidades en tiempo real vía WebSockets.

## Base URL

```
http://localhost:8000/api
```

## Autenticación

### JWT Bearer Token
Todos los endpoints (excepto login) requieren autenticación:

```
Authorization: Bearer <token>
```

### Obtener Token
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=123456
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "rol": 1,
  "username": "admin"
}
```

## Endpoints Principales

### Autenticación

#### POST `/auth/login`
Autenticar usuario y obtener token JWT.

**Body (form-data):**
- `username`: string
- `password`: string

**Respuesta 200:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "rol": number,
  "username": "string"
}
```

#### GET `/auth/me`
Obtener información del usuario actual.

**Headers:**
- `Authorization: Bearer <token>`

**Respuesta 200:**
```json
{
  "id_usuario": 1,
  "username": "admin",
  "email": "admin@example.com",
  "id_rol": 1,
  "activo": true,
  "creado_en": "2024-01-01T00:00:00Z"
}
```

### Empleados

#### GET `/empleados/`
Listar todos los empleados activos.

**Respuesta 200:**
```json
[
  {
    "id_empleado": 1,
    "bio_id": "001",
    "nombre": "Juan Pérez",
    "cedula": "123456789",
    "cargo": "Desarrollador",
    "area": "TI",
    "tarjeta_rfid": "ABC123",
    "tiene_huella": true,
    "tiene_password": false,
    "permite_huella": true,
    "permite_rfid": true,
    "permite_password": false,
    "activo": true,
    "creado_en": "2024-01-01T00:00:00Z"
  }
]
```

#### GET `/empleados/bio/{bio_id}`
Obtener empleado por ID biométrico.

**Parámetros:**
- `bio_id`: string (path)

#### GET `/empleados/cedula/{cedula}`
Buscar empleado por cédula.

**Parámetros:**
- `cedula`: string (path)

#### POST `/empleados/`
Crear nuevo empleado.

**Body:**
```json
{
  "bio_id": "002",
  "nombre": "María García",
  "cedula": "987654321",
  "cargo": "Analista",
  "area": "RRHH",
  "tarjeta_rfid": "DEF456",
  "tiene_huella": false,
  "tiene_password": true,
  "permite_huella": false,
  "permite_rfid": true,
  "permite_password": true
}
```

#### PATCH `/empleados/{bio_id}`
Actualizar empleado.

**Parámetros:**
- `bio_id`: string (path)

**Body:** Campos a actualizar (parcial)

#### DELETE `/empleados/{bio_id}`
Desactivar empleado.

**Parámetros:**
- `bio_id`: string (path)

### Registros

#### GET `/registros/`
Listar registros con filtros.

**Parámetros Query (opcionales):**
- `fecha_desde`: string (ISO 8601)
- `fecha_hasta`: string (ISO 8601)
- `empleado_id`: string
- `tipo`: "entrada" | "salida"
- `autorizado`: boolean
- `skip`: number (paginación)
- `limit`: number (paginación)

**Ejemplo:**
```
GET /registros/?fecha_desde=2024-01-01&tipo=entrada&limit=50
```

**Respuesta 200:**
```json
[
  {
    "id_registro": 1,
    "empleado_id": "001",
    "metodo": "huella",
    "tipo": "entrada",
    "fecha_hora": "2024-01-01T08:00:00Z",
    "autorizado": true,
    "motivo_bloqueo": null,
    "creado_en": "2024-01-01T08:00:00Z"
  }
]
```

#### GET `/registros/{id_registro}`
Obtener registro específico.

#### GET `/registros/estadisticas`
Obtener estadísticas de acceso.

**Parámetros Query:**
- `fecha_desde`: string
- `fecha_hasta`: string

**Respuesta 200:**
```json
{
  "total_registros": 150,
  "por_metodo": {
    "huella": 80,
    "rfid": 50,
    "password": 20
  },
  "por_hora": {
    "08:00": 15,
    "09:00": 25,
    ...
  },
  "por_dia": {
    "2024-01-01": 45,
    "2024-01-02": 38,
    ...
  }
}
```

#### GET `/registros/exportar`
Exportar registros a CSV.

**Parámetros:** Mismos que `/registros/`

**Respuesta:** Archivo CSV para descarga

### Usuarios

#### GET `/usuarios/`
Listar usuarios (admin) o usuario actual.

#### GET `/usuarios/{id_usuario}`
Obtener usuario específico.

#### POST `/usuarios/`
Crear nuevo usuario (solo admin).

**Body:**
```json
{
  "username": "nuevo_user",
  "email": "user@example.com",
  "password": "secure_password",
  "id_rol": 2
}
```

#### PATCH `/usuarios/{id_usuario}`
Actualizar usuario.

#### DELETE `/usuarios/{id_usuario}`
Desactivar usuario.

### Roles

#### GET `/roles/`
Listar roles disponibles.

**Respuesta 200:**
```json
[
  {
    "id_rol": 1,
    "nombre": "admin"
  },
  {
    "id_rol": 2,
    "nombre": "visor"
  }
]
```

#### POST `/roles/`
Crear nuevo rol (solo admin).

## WebSockets

### Conexión en Tiempo Real

**URL:** `ws://localhost:8000/ws/registros`

**Protocolo:**
- Conexión autenticada con token JWT
- Mensajes JSON con nuevos registros
- Broadcast automático a todos los clientes conectados

**Mensaje de ejemplo:**
```json
{
  "tipo": "nuevo_registro",
  "datos": {
    "id_registro": 123,
    "empleado_id": "001",
    "metodo": "huella",
    "tipo": "entrada",
    "fecha_hora": "2024-01-01T08:00:00Z",
    "autorizado": true
  }
}
```

## Códigos de Estado HTTP

- **200 OK**: Operación exitosa
- **201 Created**: Recurso creado
- **400 Bad Request**: Datos inválidos
- **401 Unauthorized**: Token inválido o faltante
- **403 Forbidden**: Permisos insuficientes
- **404 Not Found**: Recurso no encontrado
- **409 Conflict**: Violación de unicidad
- **422 Unprocessable Entity**: Validación fallida

## Rate Limiting

- Implementado en endpoints críticos
- Límite: 100 requests por minuto por IP
- Headers de respuesta incluyen límites restantes

## Versionado

- **Versión actual**: v1.0.0
- **Endpoint base**: `/api/v1/`
- **Compatibilidad**: Mantenida por 2 versiones

## Documentación Interactiva

Accede a la documentación completa en:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Consideraciones de Producción

- **HTTPS**: Siempre usar en producción
- **Rate Limiting**: Configurado por endpoint
- **Logging**: Todos los requests logueados
- **CORS**: Configurado para orígenes específicos
- **Timeouts**: Configurados para evitar hanging requests