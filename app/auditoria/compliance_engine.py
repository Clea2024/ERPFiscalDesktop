from app.auditoria.audit_result import AuditResult


class ComplianceEngine:

    def analisar(self, documento, resultados):

        compliance = []

        erros = 0
        alertas = 0
        criticos = 0

        ############################################################

        for r in resultados:

            if r.severidade == "ERRO":
                erros += 1

            elif r.severidade == "ALERTA":
                alertas += 1

            elif r.severidade == "CRITICO":
                criticos += 1

        ############################################################
        # SCORE
        ############################################################

        score = 100

        score -= erros * 5
        score -= alertas * 2
        score -= criticos * 10

        if score < 0:
            score = 0

        ############################################################
        # CLASSIFICAÇÃO
        ############################################################

        if score >= 95:

            nivel = "EXCELENTE"

        elif score >= 85:

            nivel = "BOM"

        elif score >= 70:

            nivel = "REGULAR"

        elif score >= 50:

            nivel = "RUIM"

        else:

            nivel = "CRÍTICO"

        ############################################################

        compliance.append(

            AuditResult(

                regra="COMPLIANCE",

                severidade="INFO",

                mensagem=f"Score Fiscal: {score}",

            )

        )

        compliance.append(

            AuditResult(

                regra="COMPLIANCE",

                severidade="INFO",

                mensagem=f"Nível: {nivel}",

            )

        )

        return compliance