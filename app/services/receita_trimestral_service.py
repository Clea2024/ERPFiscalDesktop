from datetime import datetime
from decimal import Decimal

from app.database.database import get_session
from app.models.fiscal_document import FiscalDocumentModel


class ReceitaTrimestralService:

    def calcular(
        self,
        company_id,
        ano,
        trimestre,
    ):

        meses_por_trimestre = {
            1: (1, 2, 3),
            2: (4, 5, 6),
            3: (7, 8, 9),
            4: (10, 11, 12),
        }

        meses = meses_por_trimestre.get(
            int(trimestre)
        )

        if not meses:

            raise ValueError(
                "Trimestre inválido."
            )

        inicio = datetime(
            int(ano),
            meses[0],
            1,
        )

        if trimestre == 1:
            fim = datetime(
                int(ano),
                4,
                1,
            )

        elif trimestre == 2:
            fim = datetime(
                int(ano),
                7,
                1,
            )

        elif trimestre == 3:
            fim = datetime(
                int(ano),
                10,
                1,
            )

        else:
            fim = datetime(
                int(ano) + 1,
                1,
                1,
            )

        db = get_session()

        try:

            documentos = (
                db.query(
                    FiscalDocumentModel
                )
                .filter(
                    FiscalDocumentModel.company_id
                    == company_id,
                    FiscalDocumentModel.data_emissao
                    >= inicio,
                    FiscalDocumentModel.data_emissao
                    < fim,
                )
                .all()
            )

            total = Decimal("0.00")

            por_origem = {}

            for documento in documentos:

                valor = Decimal(
                    str(
                        documento.valor_total
                        or 0
                    )
                )

                total += valor

                origem = (
                    documento.origem
                    or "NAO_INFORMADA"
                )

                por_origem[
                    origem
                ] = (
                    por_origem.get(
                        origem,
                        Decimal("0.00"),
                    )
                    + valor
                )

            return {
                "company_id": company_id,
                "ano": ano,
                "trimestre": trimestre,
                "inicio": inicio,
                "fim": fim,
                "quantidade_documentos": len(
                    documentos
                ),
                "receita_total": total,
                "por_origem": por_origem,
            }

        finally:

            db.close()
