from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.empleado import router_empleado 
from routers.registro import router_registro
from routers.rol import router_roles
from routers.usuario import router_usuario
from routers.auth import router_auth



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Api biometrico", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la Api biometrico"}



app.include_router(router_auth)
app.include_router(router_roles)
app.include_router(router_empleado )
app.include_router(router_usuario)
app.include_router(router_registro)