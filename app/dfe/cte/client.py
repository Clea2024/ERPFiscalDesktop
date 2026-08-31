import logging

from lxml import etree
from zeep import Client

from app.sefaz.certificado import Certificado
from app.sefaz.transport import SefazTransport


class CTeClient:

    NAMESPACE = (
        "http://www.portalfiscal.inf.br/cte"
    )

    def __init__(
        self,
        certificado_path: str,
        senha: str,
        ambiente: str = "producao",
        uf: str = "CE",
    ):

        self.certificado_path = certificado_path
        self.senha = senha
        self.ambiente = ambiente.lower()
        self.uf = uf.upper()

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

    ############################################################
    # CONECTAR CERTIFICADO
    ############################################################

    def conectar(self):

        self.certificado.validar()

        self._session = (
            self.transport.get_session()
        )

        return True

    ############################################################
    # ENDPOINT
    ############################################################

    def endpoint_distribuicao(self):

        if self.ambiente == "producao":

            return (
                "https://www1.cte.fazenda.gov.br/"
                "CTeDistribuicaoDFe/"
                "CTeDistribuicaoDFe.asmx"
            )

        return (
            "https://hom1.cte.fazenda.gov.br/"
            "CTeDistribuicaoDFe/"
            "CTeDistribuicaoDFe.asmx"
        )

    ############################################################
    # CARREGAR WSDL
    ############################################################

    def carregar_wsdl(self):

        if self._session is None:

            raise RuntimeError(
                "Conecte o certificado primeiro."
            )

        wsdl = (
            self.endpoint_distribuicao()
            + "?WSDL"
        )

        self.client = Client(
            wsdl=wsdl,
            transport=(
                self.transport.get_transport()
            ),
        )

        return self.client

    ############################################################
    # CONSULTAR POR ÚLTIMO NSU
    ############################################################

    def consultar_distribuicao(
        self,
        cnpj: str,
        ultimo_nsu: str = "000000000000000",
    ):

        if self.client is None:

            raise RuntimeError(
                "Carregue o WSDL primeiro."
            )

        cnpj = "".join(
            caractere
            for caractere in str(cnpj)
            if caractere.isdigit()
        )

        if len(cnpj) != 14:

            raise ValueError(
                "CNPJ deve possuir 14 dígitos."
            )

        ultimo_nsu = str(
            ultimo_nsu
        ).zfill(15)

        dist_dfe = etree.Element(
            f"{{{self.NAMESPACE}}}distDFeInt",
            versao="1.00",
            nsmap={
                None: self.NAMESPACE
            },
        )

        ########################################################
        # AMBIENTE
        ########################################################

        tp_amb = etree.SubElement(
            dist_dfe,
            f"{{{self.NAMESPACE}}}tpAmb",
        )

        tp_amb.text = (
            "1"
            if self.ambiente == "producao"
            else "2"
        )

        ########################################################
        # CÓDIGO UF AUTOR
        ########################################################

        c_uf = etree.SubElement(
            dist_dfe,
            f"{{{self.NAMESPACE}}}cUFAutor",
        )

        # Ceará
        c_uf.text = "23"

        ########################################################
        # CNPJ
        ########################################################

        elemento_cnpj = etree.SubElement(
            dist_dfe,
            f"{{{self.NAMESPACE}}}CNPJ",
        )

        elemento_cnpj.text = cnpj

        ########################################################
        # DISTRIBUIÇÃO POR NSU
        ########################################################

        dist_nsu = etree.SubElement(
            dist_dfe,
            f"{{{self.NAMESPACE}}}distNSU",
        )

        ult_nsu = etree.SubElement(
            dist_nsu,
            f"{{{self.NAMESPACE}}}ultNSU",
        )

        ult_nsu.text = ultimo_nsu

        ########################################################
        # CHAMADA SOAP
        ########################################################

        operacao = getattr(
            self.client.service,
            "cteDistDFeInteresse",
            None,
        )

        if operacao is None:

            raise RuntimeError(
                "Operação cteDistDFeInteresse "
                "não encontrada no WSDL."
            )

        return operacao(
            cteDadosMsg={
                "_value_1": dist_dfe
            }
        )

    ############################################################
    # DESCONECTAR
    ############################################################

    def desconectar(self):

        if self._session is not None:

            try:
                self._session.close()
            except Exception:
                pass

        self._session = None
        self.client = None