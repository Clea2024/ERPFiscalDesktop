from app.auditoria.audit_result import AuditResult


class DIFALRule:

    def validar(self, documento, item):

        resultados = []

        uf_emitente = str(
            getattr(documento, "uf_emitente", "")
        ).upper()

        uf_destinatario = str(
            getattr(documento, "uf_destinatario", "")
        ).upper()

        consumidor_final = bool(
            getattr(documento, "consumidor_final", False)
        )

        valor_difal = float(
            getattr(item, "valor_difal", 0)
        )

        valor_fcp = float(
            getattr(item, "valor_fcp", 0)
        )

        ########################################################
        # Operação Interestadual
        ########################################################

        if uf_emitente == uf_destinatario:

            return resultados

        ########################################################
        # Consumidor Final
        ########################################################

        if not consumidor_final:

            return resultados

        ########################################################
        # DIFAL
        ########################################################

        if valor_difal <= 0:

            resultados.append(

                AuditResult(
                    regra="DIFAL",
                    severidade="ALERTA",
                    mensagem="Operação interestadual para consumidor final sem DIFAL.",
                    item=item.numero_item,
                    sugestao="Verificar EC 87/2015 e legislação vigente."
                )

            )

        else:

            resultados.append(

                AuditResult(
                    regra="DIFAL",
                    severidade="SUCESSO",
                    mensagem="DIFAL informado.",
                    item=item.numero_item,
                )

            )

        ########################################################
        # FCP
        ########################################################

        if valor_fcp < 0:

            resultados.append(

                AuditResult(
                    regra="FCP",
                    severidade="ERRO",
                    mensagem="Valor do FCP negativo.",
                    item=item.numero_item,
                )

            )

        return resultados