# Documentación del Proyecto Biométrico Panel

## Descripción General

Este proyecto implementa un sistema completo de control de acceso biométrico utilizando el dispositivo VTA-70075. El sistema permite la gestión remota de empleados, registros de asistencia en tiempo real y administración de permisos de acceso a través de una interfaz web.

## Características Principales

- **Control de Acceso Biométrico**: Integración con dispositivo VTA-70075 vía TCP/IP
- **Gestión de Empleados**: CRUD completo de empleados con métodos de autenticación
- **Registros en Tiempo Real**: WebSockets para actualizaciones en vivo
- **Autenticación y Autorización**: JWT con roles de usuario
- **Reportes y Estadísticas**: Exportación de datos y análisis
- **Arquitectura Modular**: Backend en FastAPI con PostgreSQL

## Estructura del Proyecto

```
biometrico-panel/
├── README.md                 # Documentación general del proyecto
├── backend/                  # Código del servidor backend
│   ├── main.py              # Punto de entrada de la aplicación FastAPI
│   ├── database.py          # Configuración de la base de datos
│   ├── tcp_server.py       # Servidor TCP para comunicación con dispositivo
│   ├── websocket_manager.py # Gestión de conexiones WebSocket
│   ├── usuarioadmin.py      # Usuario administrador por defecto
│   ├── clave.py             # Utilidades de encriptación
│   ├── controllers/         # Lógica de negocio
│   ├── core/                # Configuraciones y dependencias centrales
│   ├── models/              # Modelos de datos SQLAlchemy
│   ├── routers/             # Endpoints de la API REST
│   ├── schemas/             # Esquemas Pydantic para validación
│   └── services/            # Servicios de negocio
├── test/                    # Pruebas del sistema
└── docs/                    # Documentación técnica (este directorio)
    ├── index.md            # Esta página
    ├── architecture.md     # Arquitectura del sistema
    ├── database.md         # Esquema de base de datos
    ├── api/                # Documentación de la API
    └── modules/            # Documentación de módulos
```

## Tecnologías Utilizadas

- **Backend**: FastAPI (Python)
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Autenticación**: JWT (JSON Web Tokens)
- **WebSockets**: Para comunicación en tiempo real
- **Comunicación TCP**: Para integración con dispositivo biométrico

## Guía de Inicio Rápido

1. Instalar dependencias: `pip install -r backend/requirements.txt`
2. Configurar variables de entorno
3. Ejecutar la aplicación: `python backend/main.py`
4. Acceder a la documentación API en `http://localhost:8000/docs`

## Navegación de la Documentación

### Arquitectura y Diseño
- [Arquitectura del Sistema](architecture.md)
- [Esquema de Base de Datos](database.md)

### Módulos del Backend
- [Módulo Backend](modules/backend.md)
- [Modelos de Datos](modules/models.md)
- [Routers API](modules/routers.md)
- [Schemas Pydantic](modules/schemas.md)
- [Controladores](modules/controllers.md)
- [Servicios de Negocio](modules/services.md)
- [Configuraciones Core](modules/core.md)

### API y Despliegue
- [Referencia de Endpoints](api/endpoints.md)
- [Guía de Despliegue](deployment.md)

## Roles y Permisos

El sistema incluye dos roles principales:

- **Admin**: Acceso completo a todas las funcionalidades
  - Gestión de empleados
  - Administración de usuarios
  - Configuración del sistema
  - Reportes completos

- **Visor**: Acceso de solo lectura
  - Visualización de registros
  - Reportes básicos
  - Estadísticas de acceso

## Seguridad

- **Autenticación JWT**: Tokens con expiración configurable
- **Encriptación**: Contraseñas hasheadas con bcrypt
- **Validación**: Pydantic schemas en todas las entradas
- **CORS**: Configurado para orígenes específicos
- **Rate Limiting**: Protección contra abuso

## Monitoreo y Métricas

- **Logs**: Registro completo de operaciones
- **Health Checks**: Endpoints para verificación de estado
- **Estadísticas**: Métricas de uso del sistema
- **Alertas**: Notificaciones de eventos importantes

## Soporte

Para soporte técnico o preguntas:
- Consultar la [documentación de la API](api/endpoints.md)
- Revisar la [guía de despliegue](deployment.md)
- Verificar logs del sistema
- Contactar al equipo de desarrollo

---

*Esta documentación se mantiene actualizada con el código fuente del proyecto.*