from app.auditoria.audit_result import AuditResult

from app.auditoria.rules.cfop_rule import CFOPRule
from app.auditoria.rules.ncm_rule import NCMRule
from app.auditoria.rules.icms_rule import ICMSRule
from app.auditoria.rules.icms_st_rule import ICMSSTRule
from app.auditoria.rules.difal_rule import DIFALRule


class FiscalValidator:

    def __init__(self):

        self.cfop_rule = CFOPRule()
        self.ncm_rule = NCMRule()
        self.icms_rule = ICMSRule()
        self.icms_st_rule = ICMSSTRule()
        self.difal_rule = DIFALRule()

    ############################################################
    # VALIDAR DOCUMENTO
    ############################################################

    def validar(
        self,
        documento,
    ):

        resultados = []

        ########################################################
        # VALIDAÇÕES DO DOCUMENTO
        ########################################################

        resultados.extend(
            self.validar_documento(
                documento
            )
        )

        ########################################################
        # ITENS DO DOCUMENTO
        ########################################################

        itens = getattr(
            documento,
            "itens",
            [],
        )

        if not itens:

            resultados.append(
                AuditResult(
                    regra="DOCUMENTO",
                    severidade="ALERTA",
                    mensagem=(
                        "Documento fiscal não possui itens "
                        "carregados para auditoria."
                    ),
                    codigo=getattr(
                        documento,
                        "chave",
                        "",
                    ),
                    sugestao=(
                        "Verificar se os itens do XML "
                        "foram importados."
                    ),
                )
            )

            return resultados

        ########################################################
        # AUDITAR CADA ITEM
        ########################################################

        for item in itens:

            resultados.extend(
                self.validar_item(
                    documento,
                    item,
                )
            )

        return resultados

    ############################################################
    # DOCUMENTO
    ############################################################

    def validar_documento(
        self,
        documento,
    ):

        resultados = []

        chave = str(
            getattr(
                documento,
                "chave",
                "",
            )
            or ""
        ).strip()

        ########################################################
        # CHAVE
        ########################################################

        if not chave:

            resultados.append(
                AuditResult(
                    regra="CHAVE",
                    severidade="CRITICO",
                    mensagem=(
                        "Documento sem chave de acesso."
                    ),
                    campo="Chave",
                    sugestao=(
                        "Verificar a origem do XML."
                    ),
                )
            )

        elif (
            len(chave) != 44
            or not chave.isdigit()
        ):

            resultados.append(
                AuditResult(
                    regra="CHAVE",
                    severidade="ERRO",
                    mensagem=(
                        "Chave de acesso inválida."
                    ),
                    codigo=chave,
                    valor_encontrado=chave,
                    valor_correto=(
                        "44 dígitos numéricos"
                    ),
                    campo="Chave",
                )
            )

        else:

            resultados.append(
                AuditResult(
                    regra="CHAVE",
                    severidade="SUCESSO",
                    mensagem=(
                        "Chave de acesso válida."
                    ),
                    codigo=chave,
                )
            )

        ########################################################
        # MODELO
        ########################################################

        modelo = str(
            getattr(
                documento,
                "modelo",
                "",
            )
            or ""
        ).strip()

        if modelo not in (
            "55",
            "65",
            "57",
        ):

            resultados.append(
                AuditResult(
                    regra="MODELO",
                    severidade="ALERTA",
                    mensagem=(
                        f"Modelo fiscal não reconhecido: "
                        f"{modelo or 'não informado'}."
                    ),
                    valor_encontrado=modelo,
                    valor_correto=(
                        "55, 65 ou 57"
                    ),
                )
            )

        ########################################################
        # DATA DE EMISSÃO
        ########################################################

        data_emissao = getattr(
            documento,
            "data_emissao",
            None,
        )

        if data_emissao is None:

            resultados.append(
                AuditResult(
                    regra="DATA",
                    severidade="ERRO",
                    mensagem=(
                        "Data de emissão não informada."
                    ),
                    campo="Data de emissão",
                )
            )

        ########################################################
        # VALOR TOTAL
        ########################################################

        try:

            valor_total = float(
                getattr(
                    documento,
                    "valor_total",
                    0,
                )
                or 0
            )

        except Exception:

            valor_total = -1

        if valor_total < 0:

            resultados.append(
                AuditResult(
                    regra="VALOR TOTAL",
                    severidade="ERRO",
                    mensagem=(
                        "Valor total do documento inválido."
                    ),
                    valor_encontrado=str(
                        getattr(
                            documento,
                            "valor_total",
                            "",
                        )
                    ),
                )
            )

        ########################################################
        # EMITENTE
        ########################################################

        emitente_cnpj = str(
            getattr(
                documento,
                "emitente_cnpj",
                "",
            )
            or ""
        )

        if (
            emitente_cnpj
            and (
                len(emitente_cnpj) != 14
                or not emitente_cnpj.isdigit()
            )
        ):

            resultados.append(
                AuditResult(
                    regra="CNPJ EMITENTE",
                    severidade="ERRO",
                    mensagem=(
                        "CNPJ do emitente possui "
                        "formato inválido."
                    ),
                    valor_encontrado=emitente_cnpj,
                )
            )

        return resultados

    ############################################################
    # ITEM
    ############################################################

    def validar_item(
        self,
        documento,
        item,
    ):

        resultados = []

        ########################################################
        # CFOP
        ########################################################

        try:

            resultados.extend(
                self.cfop_rule.validar(
                    item
                )
            )

        except Exception as erro:

            resultados.append(
                self.erro_regra(
                    "CFOP",
                    item,
                    erro,
                )
            )

        ########################################################
        # NCM
        ########################################################

        try:

            resultados.extend(
                self.ncm_rule.validar(
                    item
                )
            )

        except Exception as erro:

            resultados.append(
                self.erro_regra(
                    "NCM",
                    item,
                    erro,
                )
            )

        ########################################################
        # ICMS
        ########################################################

        try:

            resultados.extend(
                self.icms_rule.validar(
                    item
                )
            )

        except Exception as erro:

            resultados.append(
                self.erro_regra(
                    "ICMS",
                    item,
                    erro,
                )
            )

        ########################################################
        # ICMS-ST
        ########################################################

        try:

            resultados.extend(
                self.icms_st_rule.validar(
                    item
                )
            )

        except Exception as erro:

            resultados.append(
                self.erro_regra(
                    "ICMS-ST",
                    item,
                    erro,
                )
            )

        ########################################################
        # DIFAL / FCP
        ########################################################

        try:

            resultados.extend(
                self.difal_rule.validar(
                    documento,
                    item,
                )
            )

        except Exception as erro:

            resultados.append(
                self.erro_regra(
                    "DIFAL",
                    item,
                    erro,
                )
            )

        return resultados

    ############################################################
    # ERRO INTERNO DE REGRA
    ############################################################

    @staticmethod
    def erro_regra(
        regra,
        item,
        erro,
    ):

        return AuditResult(
            regra=regra,
            severidade="ERRO",
            mensagem=(
                f"Falha ao executar regra "
                f"{regra}: {erro}"
            ),
            item=getattr(
                item,
                "numero_item",
                None,
            ),
            sugestao=(
                "Revisar os dados importados "
                "do XML e a regra de auditoria."
            ),
        )