import logging

from requests import Session
from requests_pkcs12 import Pkcs12Adapter


class NFSeClient:

    def __init__(
        self,
        certificado_path: str,
        senha: str,
        ambiente: str = "producao",
    ):

        self.certificado_path = certificado_path
        self.senha = senha
        self.ambiente = ambiente.lower()

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self.session = None

    ############################################################
    # URL BASE
    ############################################################

    def url_documentacao(self):

        if self.ambiente == "producao":

            return (
                "https://adn.nfse.gov.br/"
                "contribuintes/docs/index.html"
            )

        return (
            "https://adn.producaorestrita.nfse.gov.br/"
            "contribuintes/docs/index.html"
        )

    ############################################################
    # CONECTAR CERTIFICADO
    ############################################################

    def conectar(self):

        session = Session()

        adapter = Pkcs12Adapter(
            pkcs12_filename=(
                self.certificado_path
            ),
            pkcs12_password=(
                self.senha
            ),
        )

        session.mount(
            "https://",
            adapter,
        )

        self.session = session

        return True

    ############################################################
    # TESTAR ACESSO
    ############################################################

    def testar_documentacao(self):

        if self.session is None:

            self.conectar()

        resposta = self.session.get(
            self.url_documentacao(),
            timeout=60,
        )

        return {
            "status_code": resposta.status_code,
            "url": resposta.url,
            "sucesso": resposta.ok,
        }

    ############################################################
    # URL BASE DA API
    ############################################################

    def api_base(self):

        if self.ambiente == "producao":

            return (
                "https://adn.nfse.gov.br/"
                "contribuintes"
            )

        return (
            "https://adn.producaorestrita.nfse.gov.br/"
            "contribuintes"
        )

    ############################################################
    # CONSULTAR DF-e POR NSU
    ############################################################

    def consultar_nsu(
        self,
        nsu,
    ):

        if self.session is None:

            self.conectar()

        nsu = str(
            nsu
        ).strip()

        if not nsu:

            raise ValueError(
                "NSU não informado."
            )

        url = (
            f"{self.api_base()}"
            f"/DFe/{nsu}"
        )

        resposta = self.session.get(
            url,
            timeout=60,
            headers={
                "Accept": (
                    "application/json, "
                    "application/xml, "
                    "text/xml, */*"
                )
            },
        )

        return resposta
    ############################################################
    # DESCONECTAR
    ############################################################

    def desconectar(self):

        if self.session is not None:

            self.session.close()

        self.session = None