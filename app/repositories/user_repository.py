from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(User).order_by(User.nome).all()

    def buscar_por_id(self, id_usuario):
        return self.db.query(User).filter(User.id == id_usuario).first()

    def buscar_por_login(self, login):
        return self.db.query(User).filter(User.login == login).first()

    def inserir(self, usuario):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def atualizar(self):
        self.db.commit()

    def excluir(self, usuario):
        self.db.delete(usuario)
        self.db.commit()