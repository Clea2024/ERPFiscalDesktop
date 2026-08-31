from app.dfe.provider import DFeProvider
from app.dfe.nfse import (
    NFSeClient,
    NFSeSyncManager,
)


class NFSeProvider(DFeProvider):

    def __init__(
        self,
        certificado_path: str,
        senha: str,
        ambiente: str = "producao",
        uf: str = "CE",
    ):

        self.certificado_path = (
            certificado_path
        )

        self.senha = senha
        self.ambiente = ambiente
        self.uf = uf.upper()

        self.client = None
        self.manager = None

    ############################################################
    # NOME
    ############################################################

    @property
    def nome(self):

        return "NFS-e"

    ############################################################
    # CONECTAR
    ############################################################

    def conectar(self):

        self.client = NFSeClient(
            certificado_path=(
                self.certificado_path
            ),
            senha=self.senha,
            ambiente=self.ambiente,
        )

        self.client.conectar()

        self.manager = NFSeSyncManager(
            self.client
        )

        return True

    ############################################################
    # SINCRONIZAR
    ############################################################

    def sincronizar(
        self,
        cnpj: str,
    ):

        if self.client is None:

            self.conectar()

        if self.manager is None:

            raise RuntimeError(
                "NFSeSyncManager não inicializado."
            )

        return self.manager.sincronizar(
            cnpj
        )

    ############################################################
    # DESCONECTAR
    ############################################################

    def desconectar(self):

        if self.client is not None:

            try:

                self.client.desconectar()

            finally:

                self.client = None
                self.manager = None