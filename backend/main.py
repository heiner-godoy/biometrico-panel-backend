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

    # Arranca el servidor TCP junto con FastAPI
    tcp_task = asyncio.create_task(start_tcp_server())
    print("✅ Servidor TCP escuchando en puerto 7005")

    yield

    # Al apagar, cancela el TCP limpiamente
    tcp_task.cancel()
    try:
        await tcp_task
    except asyncio.CancelledError:
        pass
    print("🛑 Servidor detenido")


app = FastAPI(
    title="API Biométrico",
    version="1.0.0",
    lifespan=lifespan
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