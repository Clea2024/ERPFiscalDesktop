from app.auditoria.validators.fiscal_validator import FiscalValidator


class AuditEngine:

    def __init__(self):

        self.validator = FiscalValidator()

    ############################################################

    def auditar(self, documento):

        return self.validator.validar(
            documento
        )