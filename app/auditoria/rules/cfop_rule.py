from app.auditoria.audit_result import AuditResult


class CFOPRule:

    def __init__(self):

        self.cfops_entrada = {
            "1101", "1102", "1111", "1113",
            "1151", "1152", "1201", "1202",
            "1251", "1252", "1403", "1407",
            "1551", "1556", "1652", "1901",
        }

        self.cfops_saida = {
            "5101", "5102", "5103", "5105",
            "5106", "5109", "5110", "5115",
            "5401", "5403", "5405", "5409",
            "6101", "6102", "6108", "6403",
            "6404", "6405", "6949",
        }

    ############################################################

    def validar(self, item):

        resultados = []

        cfop = str(item.cfop).strip()

        ########################################################
        # CFOP vazio
        ########################################################

        if cfop == "":

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    severidade="ERRO",
                    mensagem="CFOP não informado.",
                    item=item.numero_item,
                    codigo=cfop,
                    campo="CFOP",
                    sugestao="Informar o CFOP correto."
                )
            )

            return resultados

        ########################################################
        # Tamanho inválido
        ########################################################

        if len(cfop) != 4:

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    severidade="ERRO",
                    mensagem="CFOP inválido.",
                    item=item.numero_item,
                    codigo=cfop,
                    campo="CFOP",
                    sugestao="CFOP deve possuir 4 dígitos."
                )
            )

            return resultados

        ########################################################
        # Entrada
        ########################################################

        if cfop.startswith(("1", "2", "3")):

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    severidade="SUCESSO",
                    mensagem="Operação de entrada.",
                    item=item.numero_item,
                    codigo=cfop,
                )
            )

        ########################################################
        # Saída
        ########################################################

        elif cfop.startswith(("5", "6", "7")):

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    severidade="SUCESSO",
                    mensagem="Operação de saída.",
                    item=item.numero_item,
                    codigo=cfop,
                )
            )

        ########################################################
        # Prefixo inválido
        ########################################################

        else:

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    severidade="ERRO",
                    mensagem="CFOP com prefixo inválido.",
                    item=item.numero_item,
                    codigo=cfop,
                    sugestao="Revisar o CFOP."
                )
            )

        ########################################################
        # Lista conhecida
        ########################################################

        if (
            cfop not in self.cfops_entrada
            and cfop not in self.cfops_saida
        ):

            resultados.append(
                AuditResult(
                    regra="CFOP",
                    severidade="ALERTA",
                    mensagem="CFOP não consta na lista inicial do ERP.",
                    item=item.numero_item,
                    codigo=cfop,
                    sugestao="Verificar tabela oficial da SEFAZ."
                )
            )

        return resultados