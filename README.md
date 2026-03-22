# biometrico-panel
Este sistema permite administrar un dispositivo biométrico VTA-70075 completamente desde un panel web, sin necesidad de USB ni software propietario. El dispositivo se conecta por Ethernet a la red local y envía los registros de entrada/salida automáticamente al servidor mediante protocolo TCP.

# Panel Biométrico VTA-70075

Sistema de control de acceso con biométrico, huellas dactilares y tarjetas RFID. Backend en FastAPI + PostgreSQL, frontend en Angular.

---

## Tabla de contenidos

- [Descripción general](#descripción-general)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación del backend](#instalación-del-backend)
- [Instalación del frontend](#instalación-del-frontend)
- [Configuración del biométrico](#configuración-del-biométrico)
- [Variables de entorno](#variables-de-entorno)
- [Endpoints de la API](#endpoints-de-la-api)
- [WebSocket tiempo real](#websocket-tiempo-real)
- [Roles y permisos](#roles-y-permisos)
- [Acceso remoto](#acceso-remoto)
- [Estructura del proyecto](#estructura-del-proyecto)

---

## Descripción general

Este sistema permite administrar un dispositivo biométrico VTA-70075 completamente desde un panel web, sin necesidad de USB ni software propietario. El dispositivo se conecta por Ethernet a la red local y envía los registros de entrada/salida automáticamente al servidor mediante protocolo TCP.

**Funcionalidades principales:**

- Registros de entrada y salida en tiempo real vía WebSocket
- Soporte para huella dactilar y tarjeta RFID por empleado
- Restricción de métodos de acceso por empleado (bloquear huella o RFID individualmente)
- Alertas automáticas de accesos bloqueados
- Gestión completa de empleados (CRUD)
- Exportación de reportes en CSV
- Estadísticas por método, hora y día
- Autenticación con JWT y roles (admin / visor)
- Acceso remoto vía VPN o IP pública

---

## Arquitectura

```
[Biométrico VTA-70075]
        |
        | TCP puerto 7005 (red LAN)
        |
[PC Servidor local]
        |
        ├── tcp_server.py        → recibe datos del biométrico
        ├── FastAPI (puerto 8000) → API REST + WebSocket
        ├── PostgreSQL (puerto 5432) → base de datos
        |
        | HTTP / WebSocket
        |
[Navegador — Angular]
        |
        ├── /login
        ├── /registros   → tiempo real
        ├── /empleados   → CRUD
        ├── /alertas     → accesos bloqueados
        └── /reportes    → exportar CSV / estadísticas
```

---

## Requisitos

### Backend
- Python 3.11 o superior
- PostgreSQL 14 o superior

### Frontend
- Node.js 18 o superior
- Angular CLI 17 o superior

### Red
- Biométrico y servidor en la misma red LAN
- Puerto 7005 abierto en el firewall local (TCP entrante)
- Puerto 8000 abierto para el panel web

---

## Instalación del backend

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/biometrico-panel.git
cd biometrico-panel/backend
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos en PostgreSQL

Abre pgAdmin o la consola `psql` y ejecuta:

```sql
CREATE DATABASE biometrico;
CREATE USER admin_bio WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE biometrico TO admin_bio;
```

### 5. Configurar variables de entorno

```bash
# Windows
copy .env.example .env

# Linux / Mac
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales. Ver sección [Variables de entorno](#variables-de-entorno).

### 6. Arrancar el servidor

```bash
python main.py
```

El servidor crea las tablas automáticamente en el primer arranque y genera un usuario administrador inicial:

```
usuario: admin
contraseña: admin123
```

> ⚠️ Cambia esta contraseña inmediatamente desde el panel antes de usar en producción.

### 7. Verificar que funciona

Abre en el navegador:

```
http://localhost:8000/docs
```

Verás la documentación interactiva de todos los endpoints (Swagger UI).

---

## Instalación del frontend

### 1. Instalar Angular CLI

```bash
npm install -g @angular/cli
```

### 2. Entrar a la carpeta del frontend

```bash
cd biometrico-panel/frontend
```

### 3. Instalar dependencias

```bash
npm install
```

### 4. Configurar la URL del backend

Edita `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  wsUrl:  'ws://localhost:8000/api/registros/ws',
};
```

### 5. Arrancar en desarrollo

```bash
ng serve
```

Abre en el navegador:

```
http://localhost:4200
```

### 6. Compilar para producción

```bash
ng build --configuration production
```

Los archivos compilados quedan en `dist/`. Se pueden servir con cualquier servidor web (Nginx, Apache) o directamente desde FastAPI con `StaticFiles`.

---

## Configuración del biométrico

En la pantalla del dispositivo VTA-70075, entra a:

```
Menú → Red
```

Configura los siguientes campos:

| Campo | Valor |
|-------|-------|
| ETH | Si |
| Server IP | IP de tu PC en la red local (ver abajo) |
| Server Port | 7005 |
| Server Req | No |

Para saber la IP de tu PC en Windows:

```bash
ipconfig
# Busca "Dirección IPv4" → ej: 192.168.1.100
```

> El puerto 5005 (No.Port) es el puerto en que escucha el biométrico. El Server Port (7005) es al que el dispositivo envía los datos — ese es el que debe coincidir con el backend.

---

## Variables de entorno

Copia `.env.example` a `.env` y completa los valores:

```env
# Base de datos PostgreSQL
DATABASE_URL=postgresql://admin_bio:tu_password@localhost:5432/biometrico

# JWT — usa un string largo y aleatorio, nunca compartas este valor
JWT_SECRET=reemplaza_esto_con_un_string_muy_largo_y_aleatorio
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=480

# Servidor TCP que escucha al biométrico
TCP_HOST=0.0.0.0
TCP_PORT=7005

# FastAPI
API_HOST=0.0.0.0
API_PORT=8000

# CORS — agrega la URL de Angular (separadas por coma si hay varias)
CORS_ORIGINS=http://localhost:4200,http://192.168.1.100:4200
```

Para generar un JWT_SECRET seguro:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login → retorna JWT |
| GET | `/api/auth/me` | Perfil del usuario actual |
| POST | `/api/auth/usuarios` | Crear usuario (solo admin) |

### Registros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/registros` | Listar registros con filtros |
| GET | `/api/registros/resumen` | Totales del día por método |
| WS | `/api/registros/ws` | WebSocket — tiempo real |

Parámetros de filtro disponibles en `GET /api/registros`:

| Parámetro | Tipo | Ejemplo |
|-----------|------|---------|
| `metodo` | string | `huella`, `rfid`, `huella_rfid` |
| `tipo` | string | `entrada`, `salida` |
| `solo_bloqueados` | bool | `true` |
| `fecha_desde` | string | `2025-03-01` |
| `fecha_hasta` | string | `2025-03-31` |
| `empleado_id` | string | `3` |
| `limite` | int | `200` (máx 1000) |

### Empleados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/empleados` | Listar todos los empleados |
| GET | `/api/empleados/{bio_id}` | Obtener un empleado |
| POST | `/api/empleados` | Crear empleado (admin) |
| PATCH | `/api/empleados/{bio_id}` | Actualizar empleado (admin) |
| DELETE | `/api/empleados/{bio_id}` | Desactivar empleado (admin) |

### Alertas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/alertas` | Últimos 100 accesos bloqueados |
| GET | `/api/alertas/count` | Conteo del día (badge navbar) |

### Reportes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/reportes/csv` | Descarga CSV con filtros |
| GET | `/api/reportes/estadisticas` | Datos para gráficas |

---

## WebSocket tiempo real

Angular se conecta a `ws://localhost:8000/api/registros/ws` y recibe cada nuevo registro en cuanto el biométrico lo envía.

Formato del mensaje recibido:

```json
{
  "id": 142,
  "empleado_id": "3",
  "nombre": "Juan Pérez",
  "fecha_hora": "2025-03-21 08:01:33",
  "tipo": "entrada",
  "metodo": "rfid",
  "autorizado": true,
  "motivo_bloqueo": null
}
```

Si el acceso fue bloqueado:

```json
{
  "id": 143,
  "empleado_id": "5",
  "nombre": "María López",
  "fecha_hora": "2025-03-21 08:03:10",
  "tipo": "entrada",
  "metodo": "rfid",
  "autorizado": false,
  "motivo_bloqueo": "Método RFID no autorizado"
}
```

---

## Roles y permisos

| Acción | admin | visor |
|--------|-------|-------|
| Ver registros | ✅ | ✅ |
| Ver empleados | ✅ | ✅ |
| Ver alertas | ✅ | ✅ |
| Exportar reportes | ✅ | ✅ |
| Crear empleados | ✅ | ❌ |
| Editar empleados | ✅ | ❌ |
| Desactivar empleados | ✅ | ❌ |
| Crear usuarios del panel | ✅ | ❌ |

---

## Acceso remoto

### Opción A — VPN (recomendada)

Si el administrador se conecta a la VPN de la empresa desde casa, puede acceder al panel con la misma URL que en la oficina:

```
http://192.168.1.100:8000/docs   ← backend
http://192.168.1.100:4200        ← frontend Angular
```

No requiere ninguna configuración adicional.

### Opción B — IP pública

Para acceder sin VPN desde cualquier lugar:

1. Configura port forwarding en el router de la empresa:
   - Puerto externo `8000` → `192.168.1.100:8000`
   - Puerto externo `4200` → `192.168.1.100:4200`
   - **No expongas el puerto 7005** — es solo para la red local

2. Agrega HTTPS con Cloudflare Tunnel (gratuito):

```bash
# Instalar cloudflared
# Descargar desde: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/

cloudflared tunnel login
cloudflared tunnel create biometrico
cloudflared tunnel run --url http://localhost:8000 biometrico
```

Cloudflare entrega una URL pública fija con HTTPS automático.

---

## Estructura del proyecto

```
biometrico-panel/
│
├── backend/
│   ├── main.py                  ← Punto de entrada
│   ├── database.py              ← Conexión PostgreSQL
│   ├── tcp_server.py            ← Receptor TCP del biométrico
│   ├── websocket_manager.py     ← Broadcast tiempo real
│   ├── requirements.txt
│   ├── .env.example
│   │
│   ├── core/
│   │   ├── config.py            ← Settings desde .env
│   │   ├── security.py          ← JWT + bcrypt
│   │   └── dependencies.py      ← Inyección de dependencias
│   │
│   ├── models/
│   │   ├── empleado.py          ← Tabla empleados
│   │   ├── registro.py          ← Tabla registros
│   │   └── usuario.py           ← Tabla usuarios del panel
│   │
│   ├── schemas/
│   │   ├── empleado.py          ← Validación Pydantic
│   │   ├── registro.py
│   │   └── usuario.py
│   │
│   └── routers/
│       ├── auth.py              ← Login / usuarios
│       ├── registros.py         ← Registros + WebSocket
│       ├── empleados.py         ← CRUD empleados
│       ├── alertas.py           ← Accesos bloqueados
│       └── reportes.py          ← CSV + estadísticas
│
└── frontend/                    ← Proyecto Angular
    ├── src/app/
    │   ├── auth/                ← Login, guard, JWT interceptor
    │   ├── registros/           ← Tabla tiempo real
    │   ├── empleados/           ← CRUD empleados
    │   ├── alertas/             ← Panel de alertas
    │   ├── reportes/            ← Exportar PDF / Excel
    │   └── core/                ← Services, models, WebSocket
    └── src/environments/        ← URLs del backend
```

---

## Licencia

MIT
