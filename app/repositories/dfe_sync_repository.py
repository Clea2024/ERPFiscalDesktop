from datetime import datetime

from app.models.dfe_sync_state import DFeSyncState


class DFeSyncRepository:

    def __init__(self, db):

        self.db = db

    @staticmethod
    def limpar_cnpj(cnpj):

        return "".join(
            caractere
            for caractere in str(cnpj)
            if caractere.isdigit()
        )

    def obter_ou_criar(
        self,
        cnpj,
        tipo,
    ):

        cnpj = self.limpar_cnpj(
            cnpj
        )

        tipo = str(
            tipo
        ).upper()

        estado = (
            self.db.query(DFeSyncState)
            .filter(
                DFeSyncState.cnpj == cnpj,
                DFeSyncState.tipo == tipo,
            )
            .first()
        )

        if estado is None:

            estado = DFeSyncState(
                cnpj=cnpj,
                tipo=tipo,
                ultimo_nsu="000000000000000",
                max_nsu="000000000000000",
            )

            self.db.add(
                estado
            )

            self.db.commit()

            self.db.refresh(
                estado
            )

        return estado

    def atualizar(
        self,
        estado,
        ultimo_nsu=None,
        max_nsu=None,
        cstat=None,
        motivo=None,
        bloqueado_ate=None,
    ):

        if ultimo_nsu is not None:
            estado.ultimo_nsu = str(
                ultimo_nsu
            ).zfill(15)

        if max_nsu is not None:
            estado.max_nsu = str(
                max_nsu
            ).zfill(15)

        if cstat is not None:
            estado.ultimo_cstat = str(
                cstat
            )

        if motivo is not None:
            estado.ultimo_motivo = str(
                motivo
            )

        estado.ultima_consulta = (
            datetime.now()
        )

        estado.bloqueado_ate = (
            bloqueado_ate
        )

        self.db.commit()

        self.db.refresh(
            estado
        )

        return estado