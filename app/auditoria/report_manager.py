from collections import Counter


class AuditReportManager:

    def gerar_resumo(self, documento, resultados):

        contador = Counter()

        for r in resultados:

            contador[r.severidade] += 1

        resumo = {

            "numero": getattr(
                documento,
                "numero",
                "",
            ),

            "emitente": getattr(
                documento,
                "emitente_nome",
                "",
            ),

            "itens": len(
                getattr(
                    documento,
                    "itens",
                    [],
                )
            ),

            "sucesso": contador["SUCESSO"],

            "info": contador["INFO"],

            "alertas": contador["ALERTA"],

            "erros": contador["ERRO"],

            "criticos": contador["CRITICO"],

            "total": len(resultados),

        }

        return resumo

    ###########################################################

    def agrupar_por_regra(self, resultados):

        grupos = {}

        for r in resultados:

            grupos.setdefault(
                r.regra,
                [],
            ).append(r)

        return grupos

    ###########################################################

    def listar_erros(self, resultados):

        return [

            r

            for r in resultados

            if r.severidade in (

                "ERRO",

                "CRITICO",

            )

        ]

    ###########################################################

    def listar_alertas(self, resultados):

        return [

            r

            for r in resultados

            if r.severidade == "ALERTA"

        ]