from datetime import datetime, timezone, date
from sqlalchemy.orm import Session
from models.registro import Registros, MetodoAcceso, TipoAcceso
from models.empleado import Empleados
from schemas.registro import CreateRegistro
from typing import Optional


class ServiceRegistro:

    def get_registros(
        self,
        db:              Session,
        metodo:          Optional[MetodoAcceso] = None,
        tipo:            Optional[TipoAcceso]   = None,
        solo_bloqueados: Optional[bool]         = None,
        empleado_id:     Optional[str]          = None,
        fecha_desde:     Optional[str]          = None,
        fecha_hasta:     Optional[str]          = None,
        limite:          int                    = 100,
    ):
        query = db.query(Registros)

        if metodo:
            query = query.filter(Registros.metodo == metodo)
        if tipo:
            query = query.filter(Registros.tipo == tipo)
        if solo_bloqueados is not None:
            query = query.filter(Registros.autorizado == (not solo_bloqueados))
        if empleado_id:
            query = query.filter(Registros.empleado_id == empleado_id)
        if fecha_desde:
            query = query.filter(Registros.fecha_hora >= datetime.fromisoformat(fecha_desde))
        if fecha_hasta:
            query = query.filter(Registros.fecha_hora <= datetime.fromisoformat(fecha_hasta))

        return query.order_by(Registros.fecha_hora.desc()).limit(limite).all()

    def get_registro_by_id(self, db: Session, id: int):
        return db.query(Registros).filter(
            Registros.id_registro == id
        ).first()

    def get_registros_by_empleado(self, db: Session, bio_id: str):
        return db.query(Registros).filter(
            Registros.empleado_id == bio_id
        ).all()

    def get_registros_bloqueados(self, db: Session):
        return db.query(Registros).filter(
            Registros.autorizado == False
        ).order_by(Registros.fecha_hora.desc()).limit(100).all()

    def create_registro(self, db: Session, data: CreateRegistro):
        autorizado     = True
        motivo_bloqueo = None

        empleado = db.query(Empleados).filter(
            Empleados.bio_id == data.empleado_id
        ).first()

        if not empleado:
            autorizado     = False
            motivo_bloqueo = "Empleado no registrado en el sistema"
        else:
            if not empleado.activo:
                autorizado     = False
                motivo_bloqueo = "Empleado inactivo"
            elif data.metodo in (MetodoAcceso.huella, MetodoAcceso.huella_password, MetodoAcceso.huella_rfid):
                if not empleado.permite_huella:
                    autorizado     = False
                    motivo_bloqueo = "Método huella no autorizado"
            elif data.metodo == MetodoAcceso.rfid:
                if not empleado.permite_rfid:
                    autorizado     = False
                    motivo_bloqueo = "Método RFID no autorizado"
            elif data.metodo == MetodoAcceso.password:
                if not empleado.permite_password:
                    autorizado     = False
                    motivo_bloqueo = "Método contraseña no autorizado"

        db_registro = Registros(
            **data.model_dump(),
            autorizado     = autorizado,
            motivo_bloqueo = motivo_bloqueo,
        )
        db.add(db_registro)
        db.commit()
        db.refresh(db_registro)
        return db_registro

    def get_resumen_dia(self, db: Session):
        hoy = date.today()
        registros = db.query(Registros).filter(
            Registros.fecha_hora >= datetime(hoy.year, hoy.month, hoy.day, tzinfo=timezone.utc)
        ).all()

        return {
            "total_entradas":   sum(1 for r in registros if r.tipo == TipoAcceso.entrada),
            "total_salidas":    sum(1 for r in registros if r.tipo == TipoAcceso.salida),
            "total_huella":     sum(1 for r in registros if r.metodo == MetodoAcceso.huella),
            "total_rfid":       sum(1 for r in registros if r.metodo == MetodoAcceso.rfid),
            "total_password":   sum(1 for r in registros if r.metodo == MetodoAcceso.password),
            "total_bloqueados": sum(1 for r in registros if not r.autorizado),
            "fecha":            datetime.now(timezone.utc),
        }


service_registro = ServiceRegistro()  # ← faltaba esto