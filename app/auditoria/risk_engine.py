from collections import defaultdict

from app.auditoria.audit_result import AuditResult


class RiskEngine:

    PESOS = {
        "INFO": 0,
        "SUCESSO": 0,
        "ALERTA": 2,
        "ERRO": 5,
        "CRITICO": 10,
    }

    def analisar(self, documento, resultados):

        risco_total = 0

        riscos = defaultdict(int)

        for r in resultados:

            peso = self.PESOS.get(
                r.severidade,
                0,
            )

            risco_total += peso

            riscos[r.regra] += peso

        nivel = self.classificar(
            risco_total
        )

        saida = []

        ##########################################################

        for regra, pontos in sorted(
            riscos.items()
        ):

            saida.append(

                AuditResult(

                    regra="RISCO",

                    severidade="INFO",

                    mensagem=(
                        f"{regra}: "
                        f"{pontos} pontos"
                    ),

                )

            )

        ##########################################################

        saida.append(

            AuditResult(

                regra="RISCO",

                severidade="INFO",

                mensagem=(
                    f"Risco Geral: "
                    f"{nivel}"
                ),

            )

        )

        return saida

    ############################################################

    def classificar(
        self,
        pontos,
    ):

        if pontos <= 5:

            return "MUITO BAIXO"

        if pontos <= 15:

            return "BAIXO"

        if pontos <= 30:

            return "MÉDIO"

        if pontos <= 60:

            return "ALTO"

        return "CRÍTICO"