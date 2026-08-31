from app.auditoria.audit_engine import AuditEngine
from app.auditoria.report_manager import (
    AuditReportManager,
)


class AuditService:

    def __init__(self):

        self.engine = AuditEngine()
        self.report = AuditReportManager()

    ############################################################

    def auditar_documento(
        self,
        documento,
    ):

        resultados = self.engine.auditar(
            documento
        )

        return resultados

    ############################################################

    def auditar_documentos(
        self,
        documentos,
    ):

        resultados_gerais = []

        for documento in documentos:

            resultados = (
                self.auditar_documento(
                    documento
                )
            )

            if resultados:
                resultados_gerais.extend(
                    resultados
                )

        return resultados_gerais