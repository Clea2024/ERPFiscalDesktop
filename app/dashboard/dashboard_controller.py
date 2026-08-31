
from app.database.database import get_session
from app.models.company import Company
from app.models.fiscal_document import FiscalDocumentModel
from app.models.sefaz_sync_state import SefazSyncState
from app.models.dfe_sync_state import DFeSyncState
from app.dashboard.dashboard_service import DashboardService


class DashboardController:

    def __init__(self):

        self.service = DashboardService()

    ############################################################
    # INDICADORES
    ############################################################

    def indicadores(
        self,
        company_id=None,
    ):

        db = get_session()

        try:

            ####################################################
            # DOCUMENTOS
            ####################################################

            query_documentos = (
                db.query(FiscalDocumentModel)
            )

            if company_id is not None:

                query_documentos = (
                    query_documentos.filter(
                        FiscalDocumentModel.company_id
                        == company_id
                    )
                )

            documentos = (
                query_documentos.all()
            )

            ####################################################
            # EMPRESAS
            ####################################################

            total_empresas = (
                db.query(Company)
                .count()
            )

            ####################################################
            # INDICADORES BÁSICOS
            ####################################################

            dados = (
                self.service.gerar_indicadores(
                    documentos,
                    [],
                )
            )

            dados["total_empresas"] = (
                total_empresas
            )

            ####################################################
            # STATUS NF-e / NFC-e
            ####################################################

            estado_nfe = (
                db.query(SefazSyncState)
                .order_by(
                    SefazSyncState
                    .ultima_consulta
                    .desc()
                )
                .first()
            )

            if estado_nfe is not None:

                dados["status_nfe"] = {
                    "cstat": (
                        estado_nfe.ultimo_cstat
                    ),
                    "motivo": (
                        estado_nfe.ultimo_motivo
                    ),
                    "ultima_consulta": (
                        estado_nfe.ultima_consulta
                    ),
                    "bloqueado_ate": (
                        estado_nfe.bloqueado_ate
                    ),
                }

            else:

                dados["status_nfe"] = None

            ####################################################
            # STATUS CT-e
            ####################################################

            estado_cte = (
                db.query(DFeSyncState)
                .filter(
                    DFeSyncState.tipo == "CTE"
                )
                .order_by(
                    DFeSyncState
                    .ultima_consulta
                    .desc()
                )
                .first()
            )

            if estado_cte is not None:

                dados["status_cte"] = {
                    "cstat": (
                        estado_cte.ultimo_cstat
                    ),
                    "motivo": (
                        estado_cte.ultimo_motivo
                    ),
                    "ultima_consulta": (
                        estado_cte.ultima_consulta
                    ),
                    "bloqueado_ate": (
                        estado_cte.bloqueado_ate
                    ),
                }

            else:

                dados["status_cte"] = None

            ####################################################
            # STATUS NFS-e
            ####################################################

            estado_nfse = (
                db.query(DFeSyncState)
                .filter(
                    DFeSyncState.tipo == "NFSE"
                )
                .order_by(
                    DFeSyncState
                    .ultima_consulta
                    .desc()
                )
                .first()
            )

            if estado_nfse is not None:

                dados["status_nfse"] = {
                    "cstat": (
                        estado_nfse.ultimo_cstat
                    ),
                    "motivo": (
                        estado_nfse.ultimo_motivo
                    ),
                    "ultima_consulta": (
                        estado_nfse.ultima_consulta
                    ),
                    "bloqueado_ate": (
                        estado_nfse.bloqueado_ate
                    ),
                }

            else:

                dados["status_nfse"] = None

            ####################################################
            # INTERPRETAR STATUS
            ####################################################

            dados["sync_nfe"] = (
                self.service.interpretar_status_sync(
                    dados.get(
                        "status_nfe"
                    )
                )
            )

            # NFC-e atualmente compartilha o estado
            # da distribuição NF-e.
            dados["sync_nfce"] = (
                self.service.interpretar_status_sync(
                    dados.get(
                        "status_nfe"
                    )
                )
            )

            dados["sync_cte"] = (
                self.service.interpretar_status_sync(
                    dados.get(
                        "status_cte"
                    )
                )
            )

            dados["sync_nfse"] = (
                self.service.interpretar_status_sync(
                    dados.get(
                        "status_nfse"
                    )
                )
            )

            return dados

        finally:

            db.close()

    ############################################################
    # LISTAR EMPRESAS
    ############################################################

    def listar_empresas(self):

        db = get_session()

        try:

            empresas = (
                db.query(Company)
                .order_by(
                    Company.razao_social
                )
                .all()
            )

            resultado = []

            for empresa in empresas:

                resultado.append(
                    {
                        "id": empresa.id,
                        "razao_social": (
                            empresa.razao_social
                        ),
                        "nome_fantasia": (
                            empresa.nome_fantasia
                            or ""
                        ),
                        "cnpj": empresa.cnpj,
                    }
                )

            return resultado

        finally:

            db.close()

    ############################################################
    # ÚLTIMOS DOCUMENTOS
    ############################################################

    def ultimos_documentos(
    self,
    company_id=None,
):
        db = get_session()

        try:

            documentos = (
                db.query(FiscalDocumentModel)
                .order_by(
                    FiscalDocumentModel
                    .data_emissao
                    .desc()
                )
                .limit(10)
                .all()
            )

            for documento in documentos:

                db.expunge(
                    documento
                )

            return documentos

        finally:

            db.close()

    ############################################################
    # ATUALIZAR
    ############################################################

    def atualizar(
        self,
        documentos=None,
        auditorias=None,
    ):

        return self.indicadores()