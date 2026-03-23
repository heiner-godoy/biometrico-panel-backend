from sqlalchemy.orm import Session
from models.rol import Rol
from schemas.rol import CreateRol, UpdateRol

class ServiceRol:

    def get_roles(self, db:Session):
        return db.query(Rol).all()
    
    def get_rol_by_id(self, db:Session, id: int):
        return db.query(Rol).filter(Rol.id_rol == id).first()

    def get_rol_by_name(self, db:Session, name: str):
        return db.query(Rol).filter(Rol.nombre == name).first()

    def add_rol(self, db: Session, rol:CreateRol):
        existing = self.get_rol_by_name(db, rol.nombre)
        if existing:
            raise ValueError("Rol existente")
        db_rol = Rol(**rol.model_dump())
        db.add(db_rol)
        db.commit()
        db.refresh(db_rol)
        return db_rol

    def update_rol(self, db: Session, id_rol:int,  data: UpdateRol):
        rol = self.get_rol_by_id(db, id_rol )
        if not rol:
            return None
        for campo, valor in data.model_dump(exclude_unset=True).items():
            setattr(rol, campo, valor)
        db.commit()
        db.refresh(rol)
        return rol

    def delete_rol(self, db: Session, id_rol: int):
        rol = self.get_rol_by_id(db, id_rol )
        if not rol:
            return None
        db.delete(rol)
        db.commit()
        return rol

rol_service = ServiceRol()
