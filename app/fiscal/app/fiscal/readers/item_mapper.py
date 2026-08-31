from decimal import Decimal

from app.fiscal.item import FiscalItem


class ItemMapper:

    NAMESPACE = {
        "nfe": "http://www.portalfiscal.inf.br/nfe"
    }

    ####################################################################
    # MAPEAR TODOS OS ITENS
    ####################################################################

    def map(
        self,
        inf,
    ):

        itens = []

        ns = self.NAMESPACE

        for numero_item, det in enumerate(
            inf.findall(
                "nfe:det",
                ns,
            ),
            start=1,
        ):

            item = FiscalItem()

            item.numero_item = numero_item

            ############################################################
            # PRODUTO
            ############################################################

            prod = det.find(
                "nfe:prod",
                ns,
            )

            if prod is not None:

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

            ############################################################
            # IMPOSTOS
            ############################################################

            imposto = det.find(
                "nfe:imposto",
                ns,
            )

            if imposto is not None:

                self.mapear_icms(
                    imposto,
                    item,
                )

                self.mapear_pis(
                    imposto,
                    item,
                )

                self.mapear_cofins(
                    imposto,
                    item,
                )

            itens.append(item)

        return itens

    ####################################################################
    # ICMS
    ####################################################################

    def mapear_icms(
        self,
        imposto,
        item,
    ):

        ns = self.NAMESPACE

        icms = imposto.find(
            "nfe:ICMS",
            ns,
        )

        if icms is None:
            return

        for filho in icms:

            item.origem = self.texto(
                filho.find(
                    "nfe:orig",
                    ns,
                )
            )

            item.cst_icms = self.texto(
                filho.find(
                    "nfe:CST",
                    ns,
                )
            )

            item.csosn = self.texto(
                filho.find(
                    "nfe:CSOSN",
                    ns,
                )
            )

            item.base_icms = self.decimal(
                self.texto(
                    filho.find(
                        "nfe:vBC",
                        ns,
                    )
                )
            )

            item.aliquota_icms = self.decimal(
                self.texto(
                    filho.find(
                        "nfe:pICMS",
                        ns,
                    )
                )
            )

            item.valor_icms = self.decimal(
                self.texto(
                    filho.find(
                        "nfe:vICMS",
                        ns,
                    )
                )
            )

            break

    ####################################################################
    # PIS
    ####################################################################

    def mapear_pis(
        self,
        imposto,
        item,
    ):

        ns = self.NAMESPACE

        pis = imposto.find(
            "nfe:PIS",
            ns,
        )

        if pis is None:
            return

        for filho in pis:

            item.cst_pis = self.texto(
                filho.find(
                    "nfe:CST",
                    ns,
                )
            )

            item.base_pis = self.decimal(
                self.texto(
                    filho.find(
                        "nfe:vBC",
                        ns,
                    )
                )
            )

            item.aliquota_pis = self.decimal(
                self.texto(
                    filho.find(
                        "nfe:pPIS",
                        ns,
                    )
                )
            )

            item.valor_pis = self.decimal(
                self.texto(
                    filho.find(
                        "nfe:vPIS",
                        ns,
                    )
                )
            )

            break

    ####################################################################
    # COFINS
    ####################################################################

    def mapear_cofins(
        self,
        imposto,
        item,
    ):

        ns = self.NAMESPACE

        cofins = imposto.find(
            "nfe:COFINS",
            ns,
        )

        if cofins is None:
            return

        for filho in cofins:

            item.cst_cofins = self.texto(
                filho.find(
                    "nfe:CST",
                    ns,
                )
            )

            item.base_cofins = self.decimal(
                self.texto(
                    filho.find(
                        "nfe:vBC",
                        ns,
                    )
                )
            )

            item.aliquota_cofins = self.decimal(
                self.texto(
                    filho.find(
                        "nfe:pCOFINS",
                        ns,
                    )
                )
            )

            item.valor_cofins = self.decimal(
                self.texto(
                    filho.find(
                        "nfe:vCOFINS",
                        ns,
                    )
                )
            )

            break

    ####################################################################
    # AUXILIARES
    ####################################################################

    def texto(
        self,
        elemento,
    ):

        if elemento is None:
            return ""

        if elemento.text is None:
            return ""

        return elemento.text.strip()

    def decimal(
        self,
        valor,
    ):

        if not valor:
            return Decimal("0.00")

        try:
            return Decimal(
                str(valor).replace(",", ".")
            )
        except Exception:
            return Decimal("0.00")