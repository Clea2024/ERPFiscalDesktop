from app.auditoria.audit_result import AuditResult


class ICMSSTRule:

    def validar(self, item):

        resultados = []

        cst = str(
            getattr(item, "cst_icms", "")
        ).strip()

        base_st = float(
            getattr(item, "base_icms_st", 0)
        )

        valor_st = float(
            getattr(item, "valor_icms_st", 0)
        )

        aliquota_st = float(
            getattr(item, "aliquota_icms_st", 0)
        )

        ########################################################
        # Base ST
        ########################################################

        if base_st < 0:

            resultados.append(
                AuditResult(
                    regra="ICMS-ST",
                    severidade="ERRO",
                    mensagem="Base ST negativa.",
                    item=item.numero_item,
                )
            )

        ########################################################
        # Valor ST
        ########################################################

        if valor_st < 0:

            resultados.append(
                AuditResult(
                    regra="ICMS-ST",
                    severidade="ERRO",
                    mensagem="Valor ST negativo.",
                    item=item.numero_item,
                )
            )

        ########################################################
        # Alíquota ST
        ########################################################

        if aliquota_st < 0:

            resultados.append(
                AuditResult(
                    regra="ICMS-ST",
                    severidade="ERRO",
                    mensagem="Alíquota ST inválida.",
                    item=item.numero_item,
                )
            )

        ########################################################
        # CST exige ST
        ########################################################

        if cst in ("10", "30", "60", "70"):

            if valor_st == 0:

                resultados.append(
                    AuditResult(
                        regra="ICMS-ST",
                        severidade="ALERTA",
                        mensagem="CST indica Substituição Tributária, porém o valor ST é zero.",
                        item=item.numero_item,
                    )
                )

            else:

                resultados.append(
                    AuditResult(
                        regra="ICMS-ST",
                        severidade="SUCESSO",
                        mensagem="ICMS-ST informado.",
                        item=item.numero_item,
                    )
                )

        return resultados