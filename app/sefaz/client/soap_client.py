import logging

from lxml import etree
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

        self.transport = SefazTransport(
            certificado=certificado_path,
            senha=senha,
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self.client = None
        self._session = None

    def conectar(self):

        self.certificado.validar()

        self._session = self.transport.get_session()

        self.logger.info(
            "Certificado carregado com sucesso."
        )

        return True

    @property
    def conectado(self):

        return self._session is not None

    def conectar_wsdl(self):

        endpoint = SefazConfig.get_endpoint(
            servico="NFeDistribuicaoDFe",
            ambiente=self.ambiente,
            uf="AN",
        )

        return endpoint

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

        return self.client

    def consultar_distribuicao(
        self,
        cnpj: str,
        ultimo_nsu: str = "000000000000000",
    ):

        if not self.conectado:
            raise RuntimeError(
                "Conecte primeiro à SEFAZ."
            )

        if self.client is None:
            raise RuntimeError(
                "Carregue o WSDL primeiro."
            )

        cnpj = "".join(
            caractere
            for caractere in cnpj
            if caractere.isdigit()
        )

        if len(cnpj) != 14:
            raise ValueError(
                "CNPJ deve possuir 14 dígitos."
            )

        ultimo_nsu = str(
            ultimo_nsu
        ).zfill(15)

        namespace = (
            "http://www.portalfiscal.inf.br/nfe"
        )

        dist_dfe = etree.Element(
            f"{{{namespace}}}distDFeInt",
            versao="1.01",
            nsmap={None: namespace},
        )

        tp_amb = etree.SubElement(
            dist_dfe,
            f"{{{namespace}}}tpAmb",
        )

        tp_amb.text = (
            "1"
            if self.ambiente == "producao"
            else "2"
        )

        c_uf = etree.SubElement(
            dist_dfe,
            f"{{{namespace}}}cUFAutor",
        )

        c_uf.text = "23"

        cnpj_element = etree.SubElement(
            dist_dfe,
            f"{{{namespace}}}CNPJ",
        )

        cnpj_element.text = cnpj

        dist_nsu = etree.SubElement(
            dist_dfe,
            f"{{{namespace}}}distNSU",
        )

        ult_nsu = etree.SubElement(
            dist_nsu,
            f"{{{namespace}}}ultNSU",
        )

        ult_nsu.text = ultimo_nsu

        resposta = (
            self.client.service
            .nfeDistDFeInteresse(
                nfeDadosMsg={
                    "_value_1": dist_dfe
                }
            )
        )

        return resposta

    def desconectar(self):

        if self._session is not None:
            self._session.close()

        self.client = None
        self._session = None