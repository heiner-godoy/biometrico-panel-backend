from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from routers.empleado import router as router_empleado
from routers.registro import router as router_registro
from routers.rol import router as router_roles
from routers.usuario import router as router_usuario
from routers.auth import router as router_auth
import asyncio
from tcp_server import start_tcp_server


@asynccontextmanager
async def lifespan(app: FastAPI):
    from database import crear_tablas
    crear_tablas()
    print("✅ Base de datos lista")

    async def iniciar_tcp():
        await asyncio.sleep(1)  # ← espera a que FastAPI levante primero
        await start_tcp_server()

    tcp_task = asyncio.create_task(iniciar_tcp())
    print("✅ Servidor TCP iniciando...")

    yield

    tcp_task.cancel()
    try:
        await tcp_task
    except asyncio.CancelledError:
        pass
    print("🛑 Servidor detenido")

app = FastAPI(
    title="Sistema Biométrico de Control de Acceso",
    description="API REST para gestionar registros de asistencia mediante dispositivos biométricos.",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Heiner",
        "email": "tu_correo@ejemplo.com",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth,     prefix="/api")
app.include_router(router_roles,    prefix="/api")
app.include_router(router_empleado, prefix="/api")
app.include_router(router_usuario,  prefix="/api")
app.include_router(router_registro, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API Biométrico"}