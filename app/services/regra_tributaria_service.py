from datetime import date
from decimal import Decimal

from app.database.database import get_session
from app.models.regra_lucro_presumido import (
    RegraLucroPresumido,
)


class RegraTributariaService:

    def buscar_regra(
        self,
        atividade,
        data_referencia=None,
        receita=0,
    ):

        if data_referencia is None:
            data_referencia = date.today()

        receita = Decimal(
            str(receita or 0)
        )

        db = get_session()

        try:

            query = (
                db.query(
                    RegraLucroPresumido
                )
                .filter(
                    RegraLucroPresumido.atividade
                    == atividade,
                    RegraLucroPresumido.ativa
                    == True,
                )
            )

            regras = query.all()

            candidatas = []

            for regra in regras:

                if (
                    regra.vigencia_inicio
                    and data_referencia
                    < regra.vigencia_inicio
                ):
                    continue

                if (
                    regra.vigencia_fim
                    and data_referencia
                    > regra.vigencia_fim
                ):
                    continue

                if (
                    regra.limite_receita
                    is not None
                    and receita
                    > Decimal(
                        str(
                            regra.limite_receita
                        )
                    )
                ):
                    continue

                candidatas.append(
                    regra
                )

            if not candidatas:

                return {
                    "encontrada": False,
                    "atividade": atividade,
                    "mensagem": (
                        "Regra tributária não encontrada "
                        "para a atividade, data e receita."
                    ),
                }

            regra = sorted(
                candidatas,
                key=lambda r: (
                    r.vigencia_inicio
                    or date.min
                ),
                reverse=True,
            )[0]

            return {
                "encontrada": True,
                "id": regra.id,
                "atividade": regra.atividade,
                "descricao": regra.descricao,
                "percentual_irpj": (
                    regra.percentual_irpj
                ),
                "percentual_csll": (
                    regra.percentual_csll
                ),
                "aliquota_irpj": (
                    regra.aliquota_irpj
                ),
                "aliquota_csll": (
                    regra.aliquota_csll
                ),
                "limite_adicional_irpj": (
                    regra.limite_adicional_irpj
                ),
                "aliquota_adicional_irpj": (
                    regra.aliquota_adicional_irpj
                ),
                "vigencia_inicio": (
                    regra.vigencia_inicio
                ),
                "vigencia_fim": (
                    regra.vigencia_fim
                ),
                "limite_receita": (
                    regra.limite_receita
                ),
                "fator_acrescimo_presuncao": (
                    regra.fator_acrescimo_presuncao
                ),
            }

        finally:

            db.close()