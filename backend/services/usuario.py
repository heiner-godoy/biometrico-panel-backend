from sqlalchemy.orm import Session
from models.empleado import Empleados
from schemas.empleado import CreateEmpleado, ResponseEmpleado, UpdateEmpleado

class ServiceEmpleado:
    
    def get_empleados(self, db:Session):
        return db.query(Empleados).all()

    def get_empleado_by_id(self, db: Session, id: int):
        return db.query(Empleados).filter(Empleados.id_empleado == id).first()

    def get_empleado_by_nombre(self, db: Session, nombre: str):
        return db.query(Empleados).filter(Empleados.nombre == nombre).first()

    def get_empleado_by_cedula(self, db: Session, cedula: str):
        return db.query(Empleados).filter(Empleados.cedula == cedula).first()

    def add_empleado(self, db: Session, empleado: CreateEmpleado):
        existing = self.get_empleado_by_cedula(db, Empleados.cedula)
        pass
    