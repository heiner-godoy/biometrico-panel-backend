from sqlalchemy.orm import Session
from models.usuario import Usuarios
from schemas.usuario import CreateUser, UpdateUser
from core.security import hash_password

class ServiceUsuario:

    def get_usuarios(self, db: Session):
        return db.query(Usuarios).all()

    def get_usuario_activos(self, db:Session):
        return db.query(Usuarios).filter(Usuarios.activo == True)

    def get_usuario_by_id(self, db:Session, id:int):
        return db.query(Usuarios).filter(Usuarios.id_usuario == id).first()

    def get_usuario_by_name(self, db:Session, username:str):
        return db.query(Usuarios).filter(Usuarios.username == username).first()
    
    def get_usuario_by_email(self, db:Session, email:str):
        return db.query(Usuarios).filter(Usuarios.email == email).first()

    def create_user(self, db:Session, data:CreateUser):
        correo = self.get_usuario_by_email(db, data.email )
        if correo:
            raise ValueError("Correo en ya en uso")
        usuario= data.model_dump()
        usuario["password"] = hash_password(usuario["password"])
        
        db_user = Usuarios(**usuario)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update_user(self, db: Session, id_usuario: int, data: UpdateUser):
        usuario = self.get_usuario_by_id(db, id_usuario)
        if not usuario:
            return None
        datos = data.model_dump(exclude_unset=True)
        if "password" in datos:
            datos["password"] = hash_password(datos["password"])
        for campo, valor in datos.items():
            setattr(usuario, campo, valor)
        db.commit()
        db.refresh(usuario)
        return usuario

    def delete_user(self, db:Session, id_usuario:int):
        usuario = self.get_usuario_by_id(db, id_usuario)
        if not usuario:
            return None
        usuario.activo = False
        db.commit()
        return usuario
    
service_usuarios = ServiceUsuario()