from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings


# El engine es la conexión real a PostgreSQL
# pool_pre_ping=True reconecta automáticamente si la BD se reinicia
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# SessionLocal es una fábrica — cada vez que llamas SessionLocal()
# te da una conexión nueva a la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase de la que heredan todos tus modelos
# SQLAlchemy la usa para saber qué tablas crear
Base = declarative_base()


def crear_tablas():
    """
    Crea todas las tablas en PostgreSQL si no existen.
    Se llama una vez al arrancar main.py.
    Los modelos deben importarse aquí para que SQLAlchemy los conozca.
    """
    import models.empleado   # noqa — importar para que SQLAlchemy registre la tabla
    import models.registro   # noqa
    import models.usuario    # noqa
    Base.metadata.create_all(bind=engine)