from app.database.database import get_session
from app.services.auth_service import AuthService


class LoginController:

    def __init__(self):

        self.db = get_session()

        self.auth = AuthService(
            self.db
        )

    ############################################################
    # AUTENTICAR
    ############################################################

    def autenticar(
        self,
        login,
        senha,
    ):

        usuario = self.auth.autenticar(
            login,
            senha,
        )

        return usuario

    ############################################################
    # CRIAR ADMINISTRADOR PADRÃO
    ############################################################

    def criar_admin(self):

        self.auth.criar_administrador()