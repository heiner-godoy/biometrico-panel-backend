# test_db.py  ← archivo temporal solo para probar
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()  # carga el .env

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Conectando a: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT version()"))
        version = resultado.fetchone()
        print(f"✅ Conexión exitosa")
        print(f"PostgreSQL: {version[0]}")
except Exception as e:
    print(f"❌ Error de conexión: {e}")