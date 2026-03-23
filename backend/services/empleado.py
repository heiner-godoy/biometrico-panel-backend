from sqlalchemy.orm import Session
from models.empleado import Empleados
from schemas.empleado import CreateEmpleado, UpdateEmpleado

class ServiceEmpleado:
    
    def get_empleados(self, db:Session):
        return db.query(Empleados).filter(Empleados.activo == True).all()

    def get_empleado_by_id(self, db: Session, id: int):
        return db.query(Empleados).filter(Empleados.bio_id == id).first()

    def get_empleado_by_nombre(self, db: Session, nombre: str):
        return db.query(Empleados).filter(Empleados.nombre == nombre).first()

    def get_empleado_by_cedula(self, db: Session, cedula: str):
        return db.query(Empleados).filter(Empleados.cedula == cedula).first()

    def add_empleado(self, db: Session, empleado: CreateEmpleado):
        existing = self.get_empleado_by_cedula(db, empleado.cedula)
        if existing:
            raise ValueError("El documento ya se encuentra registrado")
        db_empleado = Empleados(**empleado.model_dump())
        db.add(db_empleado)
        db.commit()
        db.refresh(db_empleado)
        return db_empleado
    
    def update_empleado(self, db: Session, data: UpdateEmpleado):
        empleado = self.get_empleado_by_id(db, data.bio_id)
        if not empleado:
            return None
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(empleado, campo, valor)
        db.commit()
        db.refresh(empleado)
        return empleado

    def delete_empleado(self, db: Session, bio_id: str):
        empleado = self.get_empleado_by_id(db, bio_id)
        if not empleado:
            return None
        empleado.activo = False  # soft delete
        db.commit()
        return empleado

empleado_service = ServiceEmpleado()