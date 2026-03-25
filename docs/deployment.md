# Guía de Despliegue

## Descripción General

Esta guía proporciona instrucciones completas para desplegar el sistema biométrico panel en diferentes entornos: desarrollo, staging y producción.

## Prerrequisitos

### Sistema Operativo
- **Linux**: Ubuntu 20.04+ o CentOS 7+
- **Windows**: 10+ (solo desarrollo)
- **macOS**: 11+ (desarrollo)

### Software Requerido
- **Python**: 3.8+
- **PostgreSQL**: 12+
- **Git**: 2.0+
- **Docker**: 20.10+ (opcional pero recomendado)

### Hardware Mínimo
- **CPU**: 1 core
- **RAM**: 2 GB
- **Disco**: 10 GB
- **Red**: Conexión LAN para dispositivo biométrico

## Instalación de Dependencias

### 1. Python y Pip
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python38 python38-pip

# Verificar instalación
python3 --version
pip3 --version
```

### 2. PostgreSQL
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib
sudo postgresql-setup initdb

# Iniciar servicio
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear usuario y base de datos
sudo -u postgres psql
CREATE USER biometrico_user WITH PASSWORD 'secure_password';
CREATE DATABASE biometrico_db OWNER biometrico_user;
GRANT ALL PRIVILEGES ON DATABASE biometrico_db TO biometrico_user;
\q
```

### 3. Git
```bash
sudo apt install git  # Ubuntu/Debian
sudo yum install git  # CentOS/RHEL
```

## Configuración del Proyecto

### 1. Clonar Repositorio
```bash
git clone https://github.com/tu-usuario/biometrico-panel.git
cd biometrico-panel
```

### 2. Crear Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

### 3. Instalar Dependencias
```bash
pip install -r backend/requirements.txt
```

### 4. Variables de Entorno
Crear archivo `.env` en `backend/`:

```bash
# Base de datos
DATABASE_URL=postgresql://biometrico_user:secure_password@localhost:5432/biometrico_db

# JWT
JWT_SECRET=tu_clave_secreta_muy_segura_aqui_min_32_caracteres
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=480

# Servidor TCP (para dispositivo biométrico)
TCP_HOST=0.0.0.0
TCP_PORT=7005

# Servidor API
API_HOST=0.0.0.0
API_PORT=8000

# CORS (para frontend)
CORS_ORIGINS=http://localhost:4200,https://tu-dominio.com
```

### 5. Generar Clave JWT Segura
```bash
# Linux/macOS
openssl rand -hex 32

# Windows (PowerShell)
[System.Web.Security.Membership]::GeneratePassword(32,0)
```

## Inicialización de la Base de Datos

### 1. Ejecutar Migraciones
```bash
cd backend
python main.py
# Las tablas se crean automáticamente al iniciar
# Presiona Ctrl+C después de ver "✅ Base de datos lista"
```

### 2. Verificar Usuario Admin
El sistema crea automáticamente un usuario admin:
- **Username**: admin
- **Password**: 123456 (cambiar en producción)

## Configuración del Dispositivo Biométrico

### 1. Conexión de Red
- Conectar dispositivo VTA-70075 a la misma red LAN
- Configurar IP estática en el dispositivo
- Verificar conectividad: `ping <ip_dispositivo>`

### 2. Configuración del Dispositivo
- Acceder al panel web del dispositivo (puerto 80)
- Configurar servidor TCP: `<ip_servidor>:7005`
- Configurar zona horaria
- Sincronizar empleados (opcional)

### 3. Prueba de Conexión
```bash
# Verificar puerto TCP abierto
netstat -tlnp | grep 7005

# Probar conexión desde dispositivo
# El dispositivo enviará paquetes automáticamente
```

## Despliegue en Desarrollo

### 1. Ejecutar la Aplicación
```bash
cd backend
source ../venv/bin/activate
python main.py
```

### 2. Verificar Funcionamiento
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **TCP Server**: Puerto 7005 activo

### 3. Probar Endpoints
```bash
# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=123456"

# Listar empleados
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/empleados/
```

## Despliegue en Producción

### Opción 1: Docker (Recomendado)

#### 1. Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 7005

CMD ["python", "main.py"]
```

#### 2. Docker Compose
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
      - "7005:7005"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/db
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=biometrico_db
      - POSTGRES_USER=biometrico_user
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### 3. Desplegar
```bash
docker-compose up -d
```

### Opción 2: Systemd (Linux)

#### 1. Crear Servicio
```bash
sudo nano /etc/systemd/system/biometrico-panel.service
```

Contenido:
```ini
[Unit]
Description=Sistema Biométrico Panel
After=network.target postgresql.service

[Service]
Type=simple
User=biometrico
Group=biometrico
WorkingDirectory=/opt/biometrico-panel/backend
Environment=PATH=/opt/biometrico-panel/venv/bin
ExecStart=/opt/biometrico-panel/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

#### 2. Instalar Servicio
```bash
sudo systemctl daemon-reload
sudo systemctl enable biometrico-panel
sudo systemctl start biometrico-panel
sudo systemctl status biometrico-panel
```

### Opción 3: Nginx + Gunicorn

#### 1. Instalar Gunicorn
```bash
pip install gunicorn
```

#### 2. Configurar Nginx
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 3. Ejecutar con Gunicorn
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Configuración de Red y Firewall

### 1. Abrir Puertos
```bash
# Ubuntu/Debian
sudo ufw allow 8000
sudo ufw allow 7005

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --permanent --add-port=7005/tcp
sudo firewall-cmd --reload
```

### 2. Configuración de Proxy Reverso
Para producción con dominio:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoreo y Logging

### 1. Logs del Sistema
```bash
# Ver logs en tiempo real
sudo journalctl -u biometrico-panel -f

# Logs de aplicación (si usas gunicorn)
tail -f /var/log/gunicorn/biometrico.log
```

### 2. Health Checks
```bash
# Endpoint de health check
curl http://localhost:8000/health

# Verificar base de datos
curl http://localhost:8000/api/empleados/ | head -20
```

### 3. Monitoreo de Recursos
```bash
# Uso de CPU y memoria
top -p $(pgrep python)

# Conexiones de red
netstat -tlnp | grep :7005
netstat -tlnp | grep :8000
```

## Backup y Recuperación

### 1. Backup de Base de Datos
```bash
# Backup completo
pg_dump -U biometrico_user -h localhost biometrico_db > backup_$(date +%Y%m%d).sql

# Backup comprimido
pg_dump -U biometrico_user -h localhost biometrico_db | gzip > backup_$(date +%Y%m%d).sql.gz
```

### 2. Restaurar Backup
```bash
# Crear base de datos limpia
dropdb -U biometrico_user biometrico_db
createdb -U biometrico_user biometrico_db

# Restaurar
psql -U biometrico_user -d biometrico_db < backup_20240101.sql
```

### 3. Backup Automático
```bash
# Cron job diario
crontab -e
# Agregar: 0 2 * * * /path/to/backup-script.sh
```

## Solución de Problemas

### Problema: Puerto 7005 ocupado
```bash
# Ver qué proceso usa el puerto
sudo lsof -i :7005
sudo kill -9 <PID>
```

### Problema: Error de conexión a BD
```bash
# Verificar servicio PostgreSQL
sudo systemctl status postgresql

# Verificar credenciales
psql -U biometrico_user -d biometrico_db -h localhost
```

### Problema: Dispositivo no conecta
```bash
# Verificar conectividad
ping <ip_dispositivo>

# Verificar puerto abierto
telnet <ip_dispositivo> 7005

# Revisar logs del servidor TCP
tail -f /var/log/biometrico-panel.log
```

### Problema: API no responde
```bash
# Verificar proceso corriendo
ps aux | grep python

# Verificar puerto
curl http://localhost:8000/health

# Reiniciar servicio
sudo systemctl restart biometrico-panel
```

## Actualizaciones

### 1. Actualizar Código
```bash
cd /opt/biometrico-panel
git pull origin main
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Migraciones de BD
```bash
# Si hay cambios en modelos
python backend/main.py  # Las tablas se actualizan automáticamente
```

### 3. Reiniciar Servicios
```bash
sudo systemctl restart biometrico-panel
```

## Seguridad en Producción

### 1. Configuración SSL/TLS
- Usar certificados Let's Encrypt
- Forzar HTTPS
- Configurar HSTS

### 2. Seguridad de Base de Datos
- Cambiar contraseña por defecto
- Usar conexiones SSL
- Limitar acceso por IP

### 3. Seguridad de Aplicación
- Cambiar JWT_SECRET
- Configurar CORS restrictivo
- Implementar rate limiting
- Mantener dependencias actualizadas

### 4. Monitoreo de Seguridad
- Logs de acceso
- Alertas de intentos de login fallidos
- Auditoría de cambios

## Soporte y Contacto

Para soporte técnico:
- **Email**: soporte@tu-empresa.com
- **Docs**: https://tu-dominio.com/docs
- **Issues**: https://github.com/tu-usuario/biometrico-panel/issues