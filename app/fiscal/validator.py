from app.auditoria.rules.cfop_rule import CFOPRule
from app.auditoria.rules.ncm_rule import NCMRule
from app.auditoria.rules.icms_rule import ICMSRule
from app.auditoria.rules.icms_st_rule import ICMSSTRule
from app.auditoria.rules.difal_rule import DIFALRule
from app.auditoria.intelligence_engine import (
    IntelligenceEngine,
)
from app.auditoria.compliance_engine import ComplianceEngine
from app.auditoria.risk_engine import (
    RiskEngine,
)

class FiscalValidator:

    def __init__(self):
        self.intelligence = IntelligenceEngine()
        self.risk = RiskEngine()

        self.compliance = ComplianceEngine()
        self.regras = [

            CFOPRule(),
            NCMRule(),
            ICMSRule(),
            ICMSSTRule(),

        ]

        self.regra_difal = DIFALRule()

    ############################################################

    def validar(self, documento):

        resultados = []

        itens = getattr(
            documento,
            "itens",
            [],
        )

        resultados.extend(
        self.intelligence.analisar(
        documento
        )
    )
        resultados.extend(

    self.compliance.analisar(
        documento,
        resultados,
        )

    )
        resultados.extend(

        self.risk.analisar(
        documento,
        resultados,
        )

    )   
        ########################################################
        # Auditoria item a item
        ########################################################

        for item in itens:

            for regra in self.regras:

                try:

                    resultados.extend(
                        regra.validar(item)
                    )

                except Exception as erro:

                    print(
                        f"{regra.__class__.__name__}: {erro}"
                    )

            ####################################################
            # DIFAL depende do documento inteiro
            ####################################################

            try:

                resultados.extend(
                    self.regra_difal.validar(
                        documento,
                        item,
                    )
                )

            except Exception as erro:

                print(
                    f"DIFALRule: {erro}"
                )

        return resultados