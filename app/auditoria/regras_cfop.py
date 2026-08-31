from app.auditoria.audit_result import AuditResult


class RegraCFOP:

    ####################################################################
    # AUDITORIA
    ####################################################################

    def validar(self, item):

        resultados = []

        ############################################################
        # CFOP obrigatório
        ############################################################

        if item.cfop == "":

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    status="ERRO",
                    mensagem="CFOP não informado.",
                    item=item.numero_item,
                )
            )

            return resultados

        ############################################################
        # Tamanho
        ############################################################

        if len(item.cfop) != 4:

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    status="ERRO",
                    mensagem=f"CFOP inválido ({item.cfop}).",
                    item=item.numero_item,
                )
            )

            return resultados

        ############################################################
        # Primeiro dígito
        ############################################################

        primeiro = item.cfop[0]

        permitidos = (
            "1",
            "2",
            "3",
            "5",
            "6",
            "7",
        )

        if primeiro not in permitidos:

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    status="ERRO",
                    mensagem=f"Primeiro dígito inválido ({item.cfop}).",
                    item=item.numero_item,
                )
            )

        ############################################################
        # Compra x Venda
        ############################################################

        if primeiro in ("1", "2", "3"):

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    status="OK",
                    mensagem="Operação de Entrada.",
                    item=item.numero_item,
                )
            )

        if primeiro in ("5", "6", "7"):

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    status="OK",
                    mensagem="Operação de Saída.",
                    item=item.numero_item,
                )
            )

        return resultados