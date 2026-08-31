from app.audit.result import (
    AuditResult,
    Severity,
)


class CFOPValidator:

    ####################################################################
    # VALIDAÇÃO
    ####################################################################

    def validar(
        self,
        documento,
    ):

        resultados = []

        cfop = getattr(
            documento,
            "cfop",
            "",
        )

        if not cfop:

            resultado = AuditResult()

            resultado.documento = documento.chave

            resultado.regra = "CFOP"

            resultado.descricao = (
                "Documento sem CFOP."
            )

            resultado.severidade = (
                Severity.ALTA
            )

            resultado.legislacao = (
                "RICMS"
            )

            resultado.sugestao = (
                "Verificar o XML."
            )

            resultado.aprovado = False

            resultados.append(
                resultado
            )

            return resultados

        ############################################################

        if len(cfop) != 4:

            resultado = AuditResult()

            resultado.documento = documento.chave

            resultado.regra = "CFOP"

            resultado.descricao = (
                "CFOP inválido."
            )

            resultado.severidade = (
                Severity.ALTA
            )

            resultado.legislacao = (
                "Tabela CFOP"
            )

            resultado.sugestao = (
                "Corrigir o CFOP."
            )

            resultado.aprovado = False

            resultados.append(
                resultado
            )

        ############################################################

        return resultados