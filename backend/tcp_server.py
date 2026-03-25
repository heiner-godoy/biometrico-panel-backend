import asyncio
from database import SessionLocal
from models.registro import Registros, MetodoAcceso, TipoAcceso  # ← Registros con S
from datetime import datetime, timezone

HOST = "0.0.0.0"
PORT = 7005

METODO_MAP = {
    0: "huella",
    1: "password",
    2: "rfid",
    3: "huella_password",
    4: "huella_rfid",
}

def parsear_paquete(data: bytes, dispositivo_ip: str):
    try:
        print(f"[TCP] Longitud : {len(data)} bytes")
        print(f"[TCP] Hex      : {' '.join(data.hex()[i:i+2] for i in range(0, len(data.hex()), 2))}")
        print(f"[TCP] Texto    : {data.decode('ascii', errors='replace')}")

        # ⚠️ Offsets pendientes — se ajustan luego con captura real
        user_id  = int.from_bytes(data[0:4],  byteorder='little')
        ts_unix  = int.from_bytes(data[4:8],  byteorder='little')
        tipo_raw = int.from_bytes(data[8:9],  byteorder='little')
        met_raw  = int.from_bytes(data[9:10], byteorder='little')

        return {
            "empleado_id":    str(user_id),
            "dispositivo_sn": dispositivo_ip,   # usamos la IP hasta tener el SN real
            "fecha_hora":     datetime.fromtimestamp(ts_unix, tz=timezone.utc),
            "tipo":           "entrada" if tipo_raw == 1 else "salida",
            "metodo":         METODO_MAP.get(met_raw, "desconocido"),
            "autorizado":     True,
            "motivo_bloqueo": None,
        }
    except Exception as e:
        print(f"[TCP] Error parseando: {e}")
        return None

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    dispositivo_ip = addr[0]
    print(f"[TCP] ✅ Biométrico conectado desde {addr}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"[TCP] Biométrico desconectado: {addr}")
                break

            print(f"[TCP] --- Paquete recibido ---")
            registro = parsear_paquete(data, dispositivo_ip)

            if registro:
                db = SessionLocal()
                try:
                    db_registro = Registros(**registro)
                    db.add(db_registro)
                    db.commit()
                    print(f"[TCP] ✅ Registro guardado: {registro}")
                except Exception as e:
                    db.rollback()
                    print(f"[TCP] ❌ Error guardando en DB: {e}")
                finally:
                    db.close()

    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"[TCP] Error inesperado: {e}")
    finally:
        writer.close()

async def start_tcp_server():
    try:
        server = await asyncio.start_server(handle_client, HOST, PORT)
        print(f"[TCP] 🟢 Escuchando en {HOST}:{PORT}")
        async with server:
            await server.serve_forever()
    except OSError as e:
        print(f"[TCP] ❌ No se pudo iniciar el servidor TCP: {e}")
    except asyncio.CancelledError:
        print("[TCP] 🛑 Servidor TCP detenido")