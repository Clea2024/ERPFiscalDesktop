from app.auditoria.audit_result import AuditResult


class IntelligenceEngine:

    def analisar(self, documento):

        resultados = []

        itens = getattr(
            documento,
            "itens",
            [],
        )

        for item in itens:

            resultados.extend(
                self.validar_cfop_ncm(item)
            )

            resultados.extend(
                self.validar_cfop_cst(item)
            )

            resultados.extend(
                self.validar_ncm_cest(item)
            )

        return resultados

    ##########################################################

    def validar_cfop_ncm(self, item):

        resultados = []

        cfop = str(
            getattr(item, "cfop", "")
        )

        ncm = str(
            getattr(item, "ncm", "")
        )

        if cfop.startswith("5") and ncm == "":

            resultados.append(

                AuditResult(

                    regra="INTELIGÊNCIA",

                    severidade="ERRO",

                    mensagem="Venda sem NCM.",

                    item=item.numero_item,

                )

            )

        return resultados

    ##########################################################

    def validar_cfop_cst(self, item):

        resultados = []

        cfop = str(
            getattr(item, "cfop", "")
        )

        cst = str(
            getattr(item, "cst_icms", "")
        )

        if cfop.startswith("6") and cst == "":

            resultados.append(

                AuditResult(

                    regra="INTELIGÊNCIA",

                    severidade="ALERTA",

                    mensagem="Operação interestadual sem CST.",

                    item=item.numero_item,

                )

            )

        return resultados

    ##########################################################

    def validar_ncm_cest(self, item):

        resultados = []

        ncm = str(
            getattr(item, "ncm", "")
        )

        cest = str(
            getattr(item, "cest", "")
        )

        if len(ncm) == 8 and cest == "":

            resultados.append(

                AuditResult(

                    regra="INTELIGÊNCIA",

                    severidade="INFO",

                    mensagem="Verificar obrigatoriedade do CEST.",

                    item=item.numero_item,

                )

            )

        return resultados