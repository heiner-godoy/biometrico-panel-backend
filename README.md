# Sistema Biométrico de Control de Acceso

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema completo de control de acceso biométrico que permite administrar el dispositivo VTA-70075 desde un panel web. Incluye gestión de empleados, registros en tiempo real, autenticación JWT y reportes avanzados.

## ✨ Características Principales

- 🔐 **Control Biométrico**: Integración completa con dispositivo VTA-70075 vía TCP/IP
- 👥 **Gestión de Empleados**: CRUD completo con métodos de autenticación flexibles
- ⚡ **Tiempo Real**: WebSockets para actualizaciones instantáneas de registros
- 🔒 **Autenticación Segura**: JWT con roles (Admin/Visor) y permisos granulares
- 📊 **Reportes Avanzados**: Estadísticas, exportación CSV y análisis de acceso
- 🏗️ **Arquitectura Modular**: Backend FastAPI + PostgreSQL, fácilmente extensible
- 🌐 **Acceso Remoto**: Compatible con VPN e IP pública
- 📱 **Interfaz Web**: Panel administrativo completo (Angular)

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8+
- PostgreSQL 12+
- Node.js 18+ (para frontend)
- Dispositivo biométrico VTA-70075 en red LAN

### Instalación

1. **Clonar repositorio**
   ```bash
   git clone https://github.com/tu-usuario/biometrico-panel.git
   cd biometrico-panel
   ```

2. **Backend - Configurar entorno**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Configurar base de datos**
   ```sql
   CREATE DATABASE biometrico_db;
   CREATE USER biometrico_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE biometrico_db TO biometrico_user;
   ```

4. **Variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con credenciales de BD y JWT_SECRET
   ```

5. **Ejecutar aplicación**
   ```bash
   python main.py
   ```

6. **Acceder al sistema**
   - API Docs: http://localhost:8000/docs
   - Usuario admin inicial: `admin` / `123456`

### Configuración del Dispositivo Biométrico

1. Acceder al menú de red del dispositivo VTA-70075
2. Configurar:
   - **Server IP**: IP del servidor en la red LAN
   - **Server Port**: `7005`
   - **ETH**: Habilitado

## 📁 Estructura del Proyecto

```
biometrico-panel/
├── backend/                  # Servidor FastAPI
│   ├── main.py              # Punto de entrada
│   ├── database.py          # Configuración BD
│   ├── tcp_server.py       # Comunicación con biométrico
│   ├── core/                # Configuraciones centrales
│   ├── models/              # Entidades SQLAlchemy
│   ├── schemas/             # Validación Pydantic
│   ├── routers/             # Endpoints REST
│   ├── controllers/         # Lógica de negocio
│   └── services/            # Servicios de aplicación
├── docs/                    # Documentación completa
├── test/                    # Pruebas del sistema
└── README.md               # Este archivo
```

## 🔧 Tecnologías

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Autenticación**: JWT (JSON Web Tokens)
- **Tiempo Real**: WebSockets
- **Comunicación**: TCP/IP con dispositivo biométrico
- **Documentación**: OpenAPI/Swagger
- **Testing**: Pytest

## 📚 Documentación

Para información detallada, consulta la documentación completa:

- **[📖 Documentación Completa](docs/index.md)** - Guía técnica detallada
- **[🏗️ Arquitectura](docs/architecture.md)** - Diseño del sistema
- **[🗄️ Base de Datos](docs/database.md)** - Esquema y modelos
- **[🔌 API Reference](docs/api/endpoints.md)** - Endpoints y ejemplos
- **[🚀 Despliegue](docs/deployment.md)** - Guías de instalación

## 🔐 Autenticación y Roles

### Roles del Sistema
- **Admin**: Control total del sistema
  - Gestión de empleados y usuarios
  - Configuración del sistema
  - Reportes completos

- **Visor**: Acceso de solo lectura
  - Visualización de registros
  - Reportes básicos
  - Estadísticas

### Seguridad
- Autenticación JWT con expiración configurable
- Contraseñas encriptadas con bcrypt
- Validación de entrada con Pydantic
- CORS configurado para orígenes específicos

## 🌟 Funcionalidades

### Gestión de Empleados
- Registro completo con datos personales
- Configuración de métodos de acceso (huella, RFID, contraseña)
- Control granular de permisos por empleado
- Estados activo/inactivo

### Registros de Acceso
- Captura automática desde dispositivo biométrico
- Registros manuales para casos especiales
- Filtros avanzados por fecha, empleado, método
- Exportación a CSV

### Reportes y Estadísticas
- Conteos por método de acceso
- Distribuciones horarias y diarias
- Alertas de accesos no autorizados
- Exportación de datos

### Comunicación en Tiempo Real
- WebSockets para actualizaciones instantáneas
- Notificaciones de nuevos registros
- Actualización automática del dashboard

## 🚀 Despliegue en Producción

### Opción Recomendada: Docker
```bash
docker-compose up -d
```

### Opciones Avanzadas
- **Systemd**: Servicio Linux nativo
- **Nginx + Gunicorn**: Servidor web con proxy reverso
- **Docker**: Contenedorizado para escalabilidad

Ver **[Guía de Despliegue](docs/deployment.md)** para instrucciones detalladas.

## 🧪 Testing

```bash
cd backend
pytest test/
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Soporte

- **📧 Email**: soporte@tu-empresa.com
- **📚 Docs**: [Documentación Completa](docs/)
- **🐛 Issues**: [GitHub Issues](https://github.com/tu-usuario/biometrico-panel/issues)

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- SQLAlchemy por el ORM robusto
- Comunidad open source

---

*Desarrollado con ❤️ para soluciones de control de acceso biométrico*
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
