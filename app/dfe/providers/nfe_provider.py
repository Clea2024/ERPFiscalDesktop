from app.dfe.provider import DFeProvider
from app.sefaz.client import SefazClient
from app.sefaz.sync import SefazSyncManager


class NFeProvider(DFeProvider):

    def __init__(
        self,
        certificado_path: str,
        senha: str,
        ambiente: str = "producao",
        uf: str = "CE",
    ):

        self.certificado_path = certificado_path
        self.senha = senha
        self.ambiente = ambiente
        self.uf = uf

        self.client = None
        self.manager = None

    ############################################################
    # NOME
    ############################################################

    @property
    def nome(self):

        return "NF-e / NFC-e"

    ############################################################
    # CONECTAR
    ############################################################

    def conectar(self):

        self.client = SefazClient(
            certificado_path=self.certificado_path,
            senha=self.senha,
            ambiente=self.ambiente,
            uf=self.uf,
        )

        self.client.conectar()

        wsdl = (
            self.client.conectar_wsdl()
            + "?WSDL"
        )

        self.client.carregar_wsdl(
            wsdl
        )

        self.manager = SefazSyncManager(
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
                "Gerenciador SEFAZ não inicializado."
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