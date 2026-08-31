import logging

from zeep import Client

from app.sefaz.certificado import Certificado
from app.sefaz.transport import SefazTransport
from app.sefaz.config import SefazConfig


class SefazClient:

    def __init__(
        self,
        certificado_path: str,
        senha: str,
        ambiente: str = "producao",
        uf: str = "CE",
    ):

        self.uf = uf.upper()
        self.ambiente = ambiente.lower()

        self.certificado = Certificado(
            certificado_path,
            senha,
        )

        self.transport = SefazTransport()

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self.client = None
        self._session = None

    ############################################################

    def conectar(self):

        self.certificado.validar()

        self._session = self.transport.get_session()

        self.logger.info(
            "Certificado carregado com sucesso."
        )

        return True

    ############################################################

    def conectar_wsdl(self):

        endpoint = SefazConfig.get_endpoint(
            servico="NFeDistribuicaoDFe",
            ambiente=self.ambiente,
            uf="AN",
        )

        self.logger.info(endpoint)

        return endpoint

    ############################################################

    def carregar_wsdl(
        self,
        wsdl: str,
    ):

        if not self.conectado:
            raise RuntimeError(
                "Conecte primeiro à SEFAZ."
            )

        self.client = Client(
            wsdl=wsdl,
            transport=self.transport.get_transport(),
        )

        self.logger.info(
            "WSDL carregado com sucesso."
        )

        return self.client

    ############################################################

    def desconectar(self):

        self.client = None
        self._session = None

        self.logger.info(
            "Sessão encerrada."
        )

    ############################################################

    @property
    def conectado(self):

        return self._session is not None