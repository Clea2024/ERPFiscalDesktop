from app.auditoria.audit_result import AuditResult


class ICMSRule:

    def validar(self, item):

        resultados = []

        ############################################################
        # CST / CSOSN
        ############################################################

        cst = str(
            getattr(item, "cst_icms", "")
        ).strip()

        csosn = str(
            getattr(item, "csosn", "")
        ).strip()

        if cst == "" and csosn == "":

            resultados.append(
                AuditResult(
                    regra="ICMS",
                    severidade="ERRO",
                    mensagem="CST/CSOSN não informado.",
                    item=item.numero_item,
                    campo="CST",
                    sugestao="Informar CST ou CSOSN."
                )
            )

        ############################################################
        # ALÍQUOTA
        ############################################################

        aliquota = float(
            getattr(item, "aliquota_icms", 0)
        )

        if aliquota < 0:

            resultados.append(
                AuditResult(
                    regra="ICMS",
                    severidade="ERRO",
                    mensagem="Alíquota negativa.",
                    item=item.numero_item,
                    campo="Aliquota ICMS",
                )
            )

        elif aliquota == 0:

            resultados.append(
                AuditResult(
                    regra="ICMS",
                    severidade="ALERTA",
                    mensagem="Alíquota zerada.",
                    item=item.numero_item,
                )
            )

        else:

            resultados.append(
                AuditResult(
                    regra="ICMS",
                    severidade="SUCESSO",
                    mensagem="Alíquota válida.",
                    item=item.numero_item,
                )
            )

        ############################################################
        # BASE
        ############################################################

        base = float(
            getattr(item, "base_icms", 0)
        )

        if base < 0:

            resultados.append(
                AuditResult(
                    regra="ICMS",
                    severidade="ERRO",
                    mensagem="Base de cálculo negativa.",
                    item=item.numero_item,
                )
            )

        ############################################################
        # VALOR ICMS
        ############################################################

        valor = float(
            getattr(item, "valor_icms", 0)
        )

        if valor < 0:

            resultados.append(
                AuditResult(
                    regra="ICMS",
                    severidade="ERRO",
                    mensagem="Valor do ICMS negativo.",
                    item=item.numero_item,
                )
            )

        ############################################################
        # CFOP
        ############################################################

        cfop = str(
            getattr(item, "cfop", "")
        )

        if cfop.startswith(("5", "6")) and aliquota == 0:

            resultados.append(
                AuditResult(
                    regra="ICMS",
                    severidade="ALERTA",
                    mensagem="Saída tributável com ICMS zerado.",
                    item=item.numero_item,
                )
            )

        ############################################################
        # CST x CFOP
        ############################################################

        if cst == "00" and aliquota == 0:

            resultados.append(
                AuditResult(
                    regra="ICMS",
                    severidade="ERRO",
                    mensagem="CST 00 com alíquota zero.",
                    item=item.numero_item,
                )
            )

        ############################################################
        # BASE x VALOR
        ############################################################

        if base == 0 and valor > 0:

            resultados.append(
                AuditResult(
                    regra="ICMS",
                    severidade="ERRO",
                    mensagem="Valor ICMS informado sem base.",
                    item=item.numero_item,
                )
            )

        return resultados