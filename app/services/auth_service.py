from sqlalchemy.orm import Session

from app.models.user import User
from app.services.password_service import PasswordService


class AuthService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    ############################################################
    # AUTENTICAR
    ############################################################

    def autenticar(
        self,
        login: str,
        senha: str,
    ):

        usuario = (
            self.db.query(User)
            .filter(
                User.login == login
            )
            .first()
        )

        if usuario is None:
            return None

        if not usuario.ativo:
            return None

        if not PasswordService.verificar(
            senha,
            usuario.senha,
        ):

            return None

        return usuario

    ############################################################
    # EXISTE ADMIN
    ############################################################

    def existe_administrador(self):

        return (
            self.db.query(User)
            .count()
            > 0
        )

    ############################################################
    # CRIAR ADMIN PADRÃO
    ############################################################

    def criar_administrador(self):

        if self.existe_administrador():
            return

        admin = User(
            nome="Administrador",
            login="admin",
            senha=PasswordService.gerar_hash(
                "admin"
            ),
            email="admin@erpfiscal.com",
            administrador=True,
            ativo=True,
        )

        self.db.add(
            admin
        )

        self.db.commit()