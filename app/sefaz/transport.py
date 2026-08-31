from requests import Session
from requests.adapters import HTTPAdapter
from requests_pkcs12 import Pkcs12Adapter
from urllib3.util.retry import Retry
from zeep.transports import Transport
from zeep import Client

from app.sefaz.config import SefazConfig


class SefazTransport:

    def __init__(
        self,
        certificado,
        senha,
        verify=True,
    ):

        self.session = Session()

        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=1,
            status_forcelist=[
                500,
                502,
                503,
                504,
            ],
        )

        http_adapter = HTTPAdapter(
            max_retries=retry
        )

        https_adapter = Pkcs12Adapter(
            pkcs12_filename=certificado,
            pkcs12_password=senha,
            max_retries=retry,
        )

        self.session.mount(
            "http://",
            http_adapter,
        )

        self.session.mount(
            "https://",
            https_adapter,
        )

        self.session.verify = verify

    ############################################################

    def get_session(self):

        return self.session

    ############################################################

    def get_transport(self):

        return Transport(
            session=self.session,
            timeout=30,
            operation_timeout=60,
        )

    ############################################################
    # CONEXÃO
    ############################################################

    def conectar(self):

        self.logger.info(
            "Validando certificado digital..."
        )

        self.certificado.validar()

        self._session = self.transport.get_session()

        if self._session is None:
            raise RuntimeError(
                "Não foi possível criar a sessão HTTPS."
            )

        self.logger.info(
            "Certificado carregado com sucesso."
        )

        return True

    ############################################################
    # ENDPOINT SEFAZ
    ############################################################

    def conectar_wsdl(self):

        endpoint = SefazConfig.get_endpoint(
            servico="NFeDistribuicaoDFe",
            ambiente=self.ambiente,
            uf="AN",
        )

        if not endpoint:
            raise RuntimeError(
                "Endpoint da SEFAZ não encontrado."
            )

        self.logger.info(
            "Endpoint SEFAZ: %s",
            endpoint,
        )

        return endpoint

    ############################################################
    # CARREGAR WSDL
    ############################################################

    def carregar_wsdl(
        self,
        wsdl: str,
    ):

        if not self.conectado:
            raise RuntimeError(
                "Conecte primeiro à SEFAZ executando conectar()."
            )

        if not wsdl:
            raise ValueError(
                "O endereço WSDL não foi informado."
            )

        zeep_transport = self.transport.get_transport()

        self.client = Client(
            wsdl=wsdl,
            transport=zeep_transport,
        )

        self.logger.info(
            "WSDL carregado com sucesso."
        )

        return self.client

    ############################################################
    # DESCONECTAR
    ############################################################

    def desconectar(self):

        if self._session is not None:
            try:
                self._session.close()
            except Exception:
                self.logger.exception(
                    "Erro ao encerrar a sessão."
                )

        self.client = None
        self._session = None

        self.logger.info(
            "Sessão SEFAZ encerrada."
        )

    ############################################################
    # PROPRIEDADE CONECTADO
    ############################################################

    @property
    def conectado(self):

        return self._session is not None