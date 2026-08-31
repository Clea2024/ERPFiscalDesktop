from datetime import datetime
from decimal import Decimal
from pathlib import Path
from xml.etree import ElementTree

from app.fiscal.document import FiscalDocument
from app.fiscal.item import FiscalItem


class FiscalParser:
    """
    Parser oficial da NF-e.

    Responsável por transformar um XML em um objeto FiscalDocument.
    """

    NAMESPACE = {
        "nfe": "http://www.portalfiscal.inf.br/nfe"
    }

    ####################################################################
    # LEITURA DO XML
    ####################################################################

    def ler_xml(
        self,
        arquivo,
    ) -> FiscalDocument:

        arquivo = Path(arquivo)

        if not arquivo.exists():

            raise FileNotFoundError(
                f"Arquivo não encontrado: {arquivo}"
            )

        tree = ElementTree.parse(arquivo)

        root = tree.getroot()

        return self.converter(root)

    ####################################################################
    # CONVERTE XML -> OBJETO
    ####################################################################

    def converter(
        self,
        root,
    ) -> FiscalDocument:

        documento = FiscalDocument()

        documento.itens = []

        documento.xml = ElementTree.tostring(
            root,
            encoding="unicode",
        )

        ns = self.NAMESPACE

        ############################################################
        # infNFe
        ############################################################

        inf = root.find(
            ".//nfe:infNFe",
            ns,
        )

        if inf is None:

            raise Exception(
                "Tag infNFe não encontrada."
            )

        ############################################################
        # Chave
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

                try:

                    documento.data_emissao = (
                        datetime.fromisoformat(data)
                    )

                except ValueError:

                    documento.data_emissao = None
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

        protocolo = root.find(
            ".//nfe:protNFe/nfe:infProt",
            ns,
        )

        if protocolo is not None:

            documento.protocolo = self.texto(
                protocolo.find(
                    "nfe:nProt",
                    ns,
                )
            )

        ############################################################
        # PREPARAÇÃO PARA LEITURA DOS ITENS
        ############################################################

        detalhes = inf.findall(
            "nfe:det",
            ns,
        )
                ############################################################
        # PRODUTOS
        ############################################################

        for det in detalhes:

            print("DET.ATTRIB =", det.attrib)


            item = FiscalItem()

            ########################################################
            # NÚMERO DO ITEM
            ########################################################

            try:

                item.numero_item = int(
                    det.attrib.get(
                        "nItem",
                        "0",
                    )
                )

            except (TypeError, ValueError):

                item.numero_item = 0

            ########################################################
            # PRODUTO
            ########################################################

            prod = det.find(
                "nfe:prod",
                ns,
            )

            if prod is None:

                continue

            item.codigo = self.texto(
                prod.find(
                    "nfe:cProd",
                    ns,
                )
            )

            item.descricao = self.texto(
                prod.find(
                    "nfe:xProd",
                    ns,
                )
            )

            item.ean = self.texto(
                prod.find(
                    "nfe:cEAN",
                    ns,
                )
            )

            item.unidade = self.texto(
                prod.find(
                    "nfe:uCom",
                    ns,
                )
            )

            item.quantidade = self.decimal(
                self.texto(
                    prod.find(
                        "nfe:qCom",
                        ns,
                    )
                )
            )

            item.valor_unitario = self.decimal(
                self.texto(
                    prod.find(
                        "nfe:vUnCom",
                        ns,
                    )
                )
            )

            item.valor_total = self.decimal(
                self.texto(
                    prod.find(
                        "nfe:vProd",
                        ns,
                    )
                )
            )

            item.desconto = self.decimal(
                self.texto(
                    prod.find(
                        "nfe:vDesc",
                        ns,
                    )
                )
            )

            item.ncm = self.texto(
                prod.find(
                    "nfe:NCM",
                    ns,
                )
            )

            item.cest = self.texto(
                prod.find(
                    "nfe:CEST",
                    ns,
                )
            )

            item.cfop = self.texto(
                prod.find(
                    "nfe:CFOP",
                    ns,
                )
            )
                        ########################################################
            # IMPOSTOS
            ########################################################

            imposto = det.find(
                "nfe:imposto",
                ns,
            )

            if imposto is not None:

                ####################################################
                # ICMS
                ####################################################

                icms = imposto.find(
                    "nfe:ICMS",
                    ns,
                )

                if icms is not None:

                    for tag in icms:

                        item.origem = self.texto(
                            tag.find(
                                "nfe:orig",
                                ns,
                            )
                        )

                        item.cst_icms = self.texto(
                            tag.find(
                                "nfe:CST",
                                ns,
                            )
                        )

                        item.csosn = self.texto(
                            tag.find(
                                "nfe:CSOSN",
                                ns,
                            )
                        )

                        item.base_icms = self.decimal(
                            self.texto(
                                tag.find(
                                    "nfe:vBC",
                                    ns,
                                )
                            )
                        )

                        item.aliquota_icms = self.decimal(
                            self.texto(
                                tag.find(
                                    "nfe:pICMS",
                                    ns,
                                )
                            )
                        )

                        item.valor_icms = self.decimal(
                            self.texto(
                                tag.find(
                                    "nfe:vICMS",
                                    ns,
                                )
                            )
                        )

                        break

                ####################################################
                # PIS
                ####################################################

                pis = imposto.find(
                    "nfe:PIS",
                    ns,
                )

                if pis is not None:

                    for tag in pis:

                        item.cst_pis = self.texto(
                            tag.find(
                                "nfe:CST",
                                ns,
                            )
                        )

                        item.base_pis = self.decimal(
                            self.texto(
                                tag.find(
                                    "nfe:vBC",
                                    ns,
                                )
                            )
                        )

                        item.aliquota_pis = self.decimal(
                            self.texto(
                                tag.find(
                                    "nfe:pPIS",
                                    ns,
                                )
                            )
                        )

                        item.valor_pis = self.decimal(
                            self.texto(
                                tag.find(
                                    "nfe:vPIS",
                                    ns,
                                )
                            )
                        )

                        break

                ####################################################
                # COFINS
                ####################################################

                cofins = imposto.find(
                    "nfe:COFINS",
                    ns,
                )

                if cofins is not None:

                    for tag in cofins:

                        item.cst_cofins = self.texto(
                            tag.find(
                                "nfe:CST",
                                ns,
                            )
                        )

                        item.base_cofins = self.decimal(
                            self.texto(
                                tag.find(
                                    "nfe:vBC",
                                    ns,
                                )
                            )
                        )

                        item.aliquota_cofins = self.decimal(
                            self.texto(
                                tag.find(
                                    "nfe:pCOFINS",
                                    ns,
                                )
                            )
                        )

                        item.valor_cofins = self.decimal(
                            self.texto(
                                tag.find(
                                    "nfe:vCOFINS",
                                    ns,
                                )
                            )
                        )

                        break

                                        ####################################################
                # REFORMA TRIBUTÁRIA - IBS / CBS
                ####################################################

                ibscbs = imposto.find(
                    "nfe:IBSCBS",
                    ns,
                )

                if ibscbs is not None:

                    valor_ibs = ibscbs.find(
                        ".//nfe:vIBS",
                        ns,
                    )

                    valor_cbs = ibscbs.find(
                        ".//nfe:vCBS",
                        ns,
                    )

                    item.ibs = self.decimal(
                        self.texto(
                            valor_ibs
                        )
                    )

                    item.cbs = self.decimal(
                        self.texto(
                            valor_cbs
                        )
                    )

                ####################################################
                # REFORMA TRIBUTÁRIA - IMPOSTO SELETIVO
                ####################################################

                grupo_is = imposto.find(
                    "nfe:IS",
                    ns,
                )

                if grupo_is is not None:

                    valor_is = grupo_is.find(
                        ".//nfe:vIS",
                        ns,
                    )

                    item.imposto_seletivo = (
                        self.decimal(
                            self.texto(
                                valor_is
                            )
                        )
                    )

            ########################################################
            # ADICIONA ITEM AO DOCUMENTO
            ########################################################

            documento.itens.append(item)

        ############################################################
        # FINALIZA
        ############################################################

        documento.origem = "XML"

        return documento

    ####################################################################
    # MÉTODOS AUXILIARES
    ####################################################################

    def texto(self, elemento):

        if elemento is None:
            return ""

        if elemento.text is None:
            return ""

        return elemento.text.strip()

    ####################################################################

    def decimal(self, valor):

        if valor in (None, ""):
            return Decimal("0.00")

        try:
            return Decimal(
                str(valor).replace(",", ".")
            )

        except Exception:
            return Decimal("0.00")