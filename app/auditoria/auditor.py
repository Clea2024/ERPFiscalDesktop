from app.audit.result import AuditResult


class FiscalAuditor:

    def __init__(self):

        self.validadores = []

    ####################################################################
    # REGISTRO DE VALIDADORES
    ####################################################################

    def registrar(
        self,
        validador,
    ):

        self.validadores.append(
            validador
        )

    ####################################################################
    # AUDITORIA
    ####################################################################

    def auditar(
        self,
        documento,
    ):

        resultados = []

        for validador in self.validadores:

            try:

                retorno = validador.validar(
                    documento
                )

                if retorno is None:

                    continue

                if isinstance(
                    retorno,
                    list,
                ):

                    resultados.extend(
                        retorno
                    )

                elif isinstance(
                    retorno,
                    AuditResult,
                ):

                    resultados.append(
                        retorno
                    )

            except Exception as erro:

                resultado = AuditResult()

                resultado.documento = (
                    documento.chave
                )

                resultado.regra = (
                    validador.__class__.__name__
                )

                resultado.descricao = str(
                    erro
                )

                resultado.aprovado = False

                resultados.append(
                    resultado
                )

        return resultados

    ####################################################################
    # SCORE
    ####################################################################

    def calcular_score(
        self,
        resultados,
    ):

        if len(resultados) == 0:

            return 100

        erros = sum(
            1
            for r in resultados
            if not r.aprovado
        )

        score = (
            (len(resultados) - erros)
            / len(resultados)
        ) * 100

        return round(score, 2)