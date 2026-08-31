from app.database.database import get_session
from app.models.tributacao_federal import TributacaoFederal
from app.services.apuracao_lucro_presumido_service import (
    ApuracaoLucroPresumidoService,
)


class TributacaoFederalRepositoryService:

    def __init__(self):

        self.apurador = ApuracaoLucroPresumidoService()

    @staticmethod
    def competencia_trimestral(
        competencia,
    ):

        ano, mes = competencia.split("-")

        mes = int(mes)

        if mes in (1, 2, 3):
            trimestre = 1

        elif mes in (4, 5, 6):
            trimestre = 2

        elif mes in (7, 8, 9):
            trimestre = 3

        elif mes in (10, 11, 12):
            trimestre = 4

        else:
            raise ValueError(
                "Competência inválida."
            )

        return (
            f"{ano}-T{trimestre}"
        )

    def apurar_e_salvar(
        self,
        company_id,
        competencia,
        atividade,
        receita,
        regime="Lucro Presumido",
        data_referencia=None,
    ):

        competencia_interna = (
            self.competencia_trimestral(
                competencia
            )
        )

        resultado = self.apurador.apurar(
            atividade=atividade,
            receita=receita,
            data_referencia=data_referencia,
        )

        if not resultado.get(
            "apurado"
        ):

            return resultado

        db = get_session()

        try:

            registro = (
                db.query(
                    TributacaoFederal
                )
                .filter(
                    TributacaoFederal.company_id
                    == company_id,
                    TributacaoFederal.competencia
                    == competencia_interna,
                )
                .first()
            )

            existente = (
                registro is not None
            )

            if registro is None:

                registro = TributacaoFederal(
                    company_id=company_id,
                    competencia=competencia_interna,
                    regime=regime,
                )

                db.add(
                    registro
                )

            registro.receita_bruta = (
                resultado["receita_bruta"]
            )

            registro.base_irpj = (
                resultado["base_irpj"]
            )

            registro.aliquota_irpj = (
                resultado.get(
                    "aliquota_irpj",
                    0,
                )
            )

            registro.adicional_irpj = (
                resultado[
                    "adicional_irpj"
                ]
            )

            registro.valor_irpj = (
                resultado["valor_irpj"]
            )

            registro.base_csll = (
                resultado["base_csll"]
            )

            registro.aliquota_csll = (
                resultado.get(
                    "aliquota_csll",
                    0,
                )
            )

            registro.valor_csll = (
                resultado["valor_csll"]
            )

            db.commit()

            db.refresh(
                registro
            )

            return {
                "salvo": True,
                "existente": existente,
                "id": registro.id,
                "company_id": registro.company_id,
                "competencia": registro.competencia,
                "receita_bruta": registro.receita_bruta,
                "valor_irpj": registro.valor_irpj,
                "valor_csll": registro.valor_csll,
                "adicional_irpj": registro.adicional_irpj,
            }

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()