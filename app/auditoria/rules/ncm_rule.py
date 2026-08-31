from app.auditoria.audit_result import AuditResult


class NCMRule:

    def validar(self, item):

        resultados = []

        ncm = str(item.ncm).strip()

        ############################################################
        # NCM obrigatório
        ############################################################

        if ncm == "":

            resultados.append(
                AuditResult(
                    regra="NCM",
                    severidade="ERRO",
                    mensagem="NCM não informado.",
                    item=item.numero_item,
                    codigo=ncm,
                    campo="NCM",
                    sugestao="Informar o NCM correto."
                )
            )

            return resultados

        ############################################################
        # Quantidade de dígitos
        ############################################################

        if len(ncm) != 8:

            resultados.append(
                AuditResult(
                    regra="NCM",
                    severidade="ERRO",
                    mensagem="NCM deve possuir 8 dígitos.",
                    item=item.numero_item,
                    codigo=ncm,
                    campo="NCM",
                    sugestao="Corrigir a classificação fiscal."
                )
            )

            return resultados

        ############################################################
        # Apenas números
        ############################################################

        if not ncm.isdigit():

            resultados.append(
                AuditResult(
                    regra="NCM",
                    severidade="ERRO",
                    mensagem="NCM possui caracteres inválidos.",
                    item=item.numero_item,
                    codigo=ncm,
                    campo="NCM",
                    sugestao="Utilizar somente números."
                )
            )

            return resultados

        ############################################################
        # Sucesso
        ############################################################

        resultados.append(
            AuditResult(
                regra="NCM",
                severidade="SUCESSO",
                mensagem="NCM válido.",
                item=item.numero_item,
                codigo=ncm,
            )
        )

        ############################################################
        # Verificação do CEST
        ############################################################

        cest = str(
            getattr(item, "cest", "")
        ).strip()

        if cest == "":

            resultados.append(
                AuditResult(
                    regra="NCM",
                    severidade="ALERTA",
                    mensagem="Produto sem CEST informado.",
                    item=item.numero_item,
                    codigo=ncm,
                    sugestao="Verificar se o NCM exige CEST."
                )
            )

        return resultados