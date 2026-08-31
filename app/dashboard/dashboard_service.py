from collections import Counter


class DashboardService:

    ############################################################
    # INTERPRETAR STATUS DE SINCRONIZAÇÃO
    ############################################################

    def interpretar_status_sync(
        self,
        estado,
    ):

        if not estado:

            return {
                "status": "AGUARDANDO",
                "cor": "#F9A825",
                "ultima_consulta": "-",
            }

        ultima_consulta = estado.get(
            "ultima_consulta"
        )

        if ultima_consulta:

            ultima_formatada = (
                ultima_consulta.strftime(
                    "%d/%m/%Y %H:%M"
                )
            )

        else:

            ultima_formatada = "-"

        if estado.get(
            "bloqueado_ate"
        ):

            return {
                "status": "BLOQUEADO",
                "cor": "#C62828",
                "ultima_consulta": ultima_formatada,
            }

        cstat = str(
            estado.get(
                "cstat",
                ""
            )
            or ""
        )

        if cstat in (
            "137",
            "138",
            "200",
        ):

            return {
                "status": "SINCRONIZADO",
                "cor": "#2E7D32",
                "ultima_consulta": ultima_formatada,
            }

        return {
            "status": "VERIFICAR",
            "cor": "#EF6C00",
            "ultima_consulta": ultima_formatada,
        }

    ############################################################
    # GERAR INDICADORES
    ############################################################

    def gerar_indicadores(
        self,
        documentos,
        auditorias,
    ):

        indicadores = {}

        ########################################################
        # DOCUMENTOS
        ########################################################

        indicadores[
            "total_documentos"
        ] = len(documentos)

        ########################################################
        # DOCUMENTOS POR TIPO
        ########################################################

        total_nfe = 0
        total_nfce = 0
        total_cte = 0
        total_nfse = 0

        for documento in documentos:

            modelo = str(
                getattr(
                    documento,
                    "modelo",
                    "",
                )
                or ""
            ).strip()

            origem = str(
                getattr(
                    documento,
                    "origem",
                    "",
                )
                or ""
            ).upper()

            if modelo == "55":

                total_nfe += 1

            elif modelo == "65":

                total_nfce += 1

            elif modelo in (
                "57",
                "67",
            ):

                total_cte += 1

            elif (
                origem == "NFSE"
                or "NFSE" in origem
                or "NFS-E" in origem
            ):

                total_nfse += 1

        indicadores[
            "total_nfe"
        ] = total_nfe

        indicadores[
            "total_nfce"
        ] = total_nfce

        indicadores[
            "total_cte"
        ] = total_cte

        indicadores[
            "total_nfse"
        ] = total_nfse
        indicadores[
            "valor_total"
        ] = sum(
            float(
                getattr(
                    documento,
                    "valor_total",
                    0,
                )
                or 0
            )
            for documento in documentos
        )

        ########################################################
        # EMPRESAS
        ########################################################

        empresas = {
            getattr(
                documento,
                "company_id",
                None,
            )
            for documento in documentos
            if getattr(
                documento,
                "company_id",
                None,
            )
            is not None
        }

        indicadores[
            "total_empresas"
        ] = len(empresas)

        ########################################################
        # ÚLTIMA IMPORTAÇÃO
        ########################################################

        datas = [
            getattr(
                documento,
                "created_at",
                None,
            )
            for documento in documentos
            if getattr(
                documento,
                "created_at",
                None,
            )
        ]

        if datas:

            ultima = max(
                datas
            )

            indicadores[
                "ultima_importacao"
            ] = ultima.strftime(
                "%d/%m/%Y %H:%M"
            )

        else:

            indicadores[
                "ultima_importacao"
            ] = "-"

        ########################################################
        # AUDITORIAS
        ########################################################

        contador = Counter()

        for resultado in auditorias:

            severidade = getattr(
                resultado,
                "severidade",
                "",
            )

            contador[
                severidade
            ] += 1

        indicadores[
            "sucesso"
        ] = contador[
            "SUCESSO"
        ]

        indicadores[
            "info"
        ] = contador[
            "INFO"
        ]

        indicadores[
            "alertas"
        ] = contador[
            "ALERTA"
        ]

        indicadores[
            "erros"
        ] = contador[
            "ERRO"
        ]

        indicadores[
            "criticos"
        ] = contador[
            "CRITICO"
        ]

        ########################################################
        # SCORE
        ########################################################

        score = 100

        score -= (
            contador["ERRO"]
            * 5
        )

        score -= (
            contador["ALERTA"]
            * 2
        )

        score -= (
            contador["CRITICO"]
            * 10
        )

        indicadores[
            "score"
        ] = max(
            score,
            0,
        )

        return indicadores