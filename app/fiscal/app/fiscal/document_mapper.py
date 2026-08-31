from datetime import datetime
from decimal import Decimal
from xml.etree.ElementTree import tostring

from app.fiscal.document import FiscalDocument
from app.fiscal.readers.item_mapper import ItemMapper


class DocumentMapper:

    NAMESPACE = {
        "nfe": "http://www.portalfiscal.inf.br/nfe"
    }

    def __init__(self):

        self.item_mapper = ItemMapper()

    ####################################################################
    # MAPEAR DOCUMENTO
    ####################################################################

    def map(self, root):

        documento = FiscalDocument()

        documento.xml = tostring(
            root,
            encoding="unicode",
        )

        ns = self.NAMESPACE

        inf = root.find(
            ".//nfe:infNFe",
            ns,
        )

        if inf is None:

            raise Exception(
                "Tag infNFe não encontrada."
            )

        ############################################################
        # CHAVE
        ############################################################

        documento.chave = (
            inf.attrib.get(
                "Id",
                "",
            )
            .replace(
                "NFe",
                "",
            )
        )

        ############################################################
        # IDE
        ############################################################

        ide = inf.find(
            "nfe:ide",
            ns,
        )

        if ide is not None:

            documento.modelo = self.texto(
                ide.find(
                    "nfe:mod",
                    ns,
                )
            )

            documento.numero = self.texto(
                ide.find(
                    "nfe:nNF",
                    ns,
                )
            )

            documento.serie = self.texto(
                ide.find(
                    "nfe:serie",
                    ns,
                )
            )

            data = self.texto(
                ide.find(
                    "nfe:dhEmi",
                    ns,
                )
            )

            if data:

                documento.data_emissao = (
                    datetime.fromisoformat(data)
                )

        ############################################################
        # EMITENTE
        ############################################################

        emit = inf.find(
            "nfe:emit",
            ns,
        )

        if emit is not None:

            documento.emitente_cnpj = self.texto(
                emit.find(
                    "nfe:CNPJ",
                    ns,
                )
            )

            documento.emitente_nome = self.texto(
                emit.find(
                    "nfe:xNome",
                    ns,
                )
            )

        ############################################################
        # DESTINATÁRIO
        ############################################################

        dest = inf.find(
            "nfe:dest",
            ns,
        )

        if dest is not None:

            documento.destinatario_cnpj = self.texto(
                dest.find(
                    "nfe:CNPJ",
                    ns,
                )
            )

            documento.destinatario_nome = self.texto(
                dest.find(
                    "nfe:xNome",
                    ns,
                )
            )

        ############################################################
        # TOTAIS
        ############################################################

        total = inf.find(
            "nfe:total/nfe:ICMSTot",
            ns,
        )

        if total is not None:

            documento.valor_total = self.decimal(
                self.texto(
                    total.find(
                        "nfe:vNF",
                        ns,
                    )
                )
            )

        ############################################################
        # PROTOCOLO
        ############################################################

        prot = root.find(
            ".//nfe:protNFe/nfe:infProt",
            ns,
        )

        if prot is not None:

            documento.protocolo = self.texto(
                prot.find(
                    "nfe:nProt",
                    ns,
                )
            )

        ############################################################
        # ITENS
        ############################################################

        documento.itens = self.item_mapper.map(
            inf
        )

        ############################################################

        documento.origem = "XML"

        return documento

    ####################################################################
    # AUXILIARES
    ####################################################################

    def texto(self, elemento):

        if elemento is None:
            return ""

        if elemento.text is None:
            return ""

        return elemento.text.strip()

    def decimal(self, valor):

        if not valor:
            return Decimal("0.00")

        try:

            return Decimal(
                str(valor).replace(",", ".")
            )

        except Exception:

            return Decimal("0.00")