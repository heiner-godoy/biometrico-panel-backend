from sqlalchemy.orm import Session
from models.registro import Registros
from models.empleado import Empleados
from schemas.registro import CreateRegistro


class ServiceRegistro:

    def get_registros(self, db: Session):
        return db.query(Registros).all()

    def get_registro_by_id(self, db: Session, id: int):
        return db.query(Registros).filter(
            Registros.id_registro == id
        ).first()

    def get_registros_by_empleado(self, db: Session, bio_id: str):
        return db.query(Registros).filter(
            Registros.empleado_id == bio_id
        ).all()

    def create_registro(self, db: Session, data: CreateRegistro):
        # 1. verificar que el empleado existe
        empleado = db.query(Empleados).filter(
            Empleados.bio_id == data.empleado_id
        ).first()

        if not empleado:
            raise ValueError("Empleado no registrado en el sistema")

        # 2. verificar que está activo
        if not empleado.activo:
            raise ValueError("Empleado inactivo")

        # 3. verificar método autorizado
        if data.metodo == "huella" and not empleado.permite_huella:
            raise ValueError("Método huella no autorizado")

        if data.metodo == "rfid" and not empleado.permite_rfid:
            raise ValueError("Método RFID no autorizado")

        # 4. guardar el registro
        db_registro = Registros(**data.model_dump())
        db.add(db_registro)
        db.commit()
        db.refresh(db_registro)
        return db_registro


service_registro = ServiceRegistro()
