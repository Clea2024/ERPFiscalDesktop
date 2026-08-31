from app.database.database import get_session
from app.models.tributacao_lucro_real import (
    TributacaoLucroReal,
)
from app.services.lucro_real_service import (
    LucroRealService,
)


class ApuracaoLucroRealService:

    def __init__(self):

        self.calculadora = LucroRealService()

    def apurar_e_salvar(
        self,
        company_id,
        periodo,
        forma_apuracao,
        receita_bruta,
        custos,
        despesas_dedutiveis,
        outras_receitas=0,
        adicoes=0,
        exclusoes=0,
        compensacoes=0,
        meses_periodo=3,
    ):

        resultado = self.calculadora.calcular(
            receita_bruta=receita_bruta,
            custos=custos,
            despesas_dedutiveis=despesas_dedutiveis,
            outras_receitas=outras_receitas,
            adicoes=adicoes,
            exclusoes=exclusoes,
            compensacoes=compensacoes,
            meses_periodo=meses_periodo,
        )

        db = get_session()

        try:

            registro = (
                db.query(
                    TributacaoLucroReal
                )
                .filter(
                    TributacaoLucroReal.company_id
                    == company_id,
                    TributacaoLucroReal.periodo
                    == periodo,
                    TributacaoLucroReal.forma_apuracao
                    == forma_apuracao,
                )
                .first()
            )

            existente = (
                registro is not None
            )

            if registro is None:

                registro = (
                    TributacaoLucroReal(
                        company_id=company_id,
                        periodo=periodo,
                        forma_apuracao=forma_apuracao,
                    )
                )

                db.add(
                    registro
                )

            registro.receita_bruta = (
                resultado["receita_bruta"]
            )

            registro.custos = (
                resultado["custos"]
            )

            registro.despesas_dedutiveis = (
                resultado[
                    "despesas_dedutiveis"
                ]
            )

            registro.outras_receitas = (
                resultado[
                    "outras_receitas"
                ]
            )

            registro.lucro_contabil = (
                resultado[
                    "lucro_contabil"
                ]
            )

            registro.adicoes = (
                resultado["adicoes"]
            )

            registro.exclusoes = (
                resultado["exclusoes"]
            )

            registro.compensacoes = (
                resultado["compensacoes"]
            )

            registro.base_irpj = (
                resultado["base_irpj"]
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
                "periodo": registro.periodo,
                "forma_apuracao": (
                    registro.forma_apuracao
                ),
                "lucro_contabil": (
                    registro.lucro_contabil
                ),
                "base_irpj": registro.base_irpj,
                "valor_irpj": registro.valor_irpj,
                "base_csll": registro.base_csll,
                "valor_csll": registro.valor_csll,
            }

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()