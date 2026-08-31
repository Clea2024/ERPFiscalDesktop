from app.database.database import get_session
from app.models.tributacao_pis_cofins import TributacaoPisCofins
from app.services.pis_cofins_service import PisCofinsService


class ApuracaoPisCofinsService:
    def __init__(self):
        self.calculadora = PisCofinsService()

    def apurar_e_salvar(
        self,
        company_id,
        competencia,
        regime_apuracao,
        receita_tributavel,
        exclusoes_base=0,
        credito_pis=0,
        credito_cofins=0,
    ):
        resultado = self.calculadora.calcular(
            receita_tributavel=receita_tributavel,
            regime_apuracao=regime_apuracao,
            exclusoes_base=exclusoes_base,
            credito_pis=credito_pis,
            credito_cofins=credito_cofins,
        )

        db = get_session()

        try:
            registro = (
                db.query(TributacaoPisCofins)
                .filter(
                    TributacaoPisCofins.company_id == company_id,
                    TributacaoPisCofins.competencia == competencia,
                )
                .first()
            )

            existente = registro is not None

            if registro is None:
                registro = TributacaoPisCofins(
                    company_id=company_id,
                    competencia=competencia,
                    regime_apuracao=resultado["regime_apuracao"],
                )
                db.add(registro)

            registro.regime_apuracao = resultado["regime_apuracao"]
            registro.receita_tributavel = resultado["receita_tributavel"]
            registro.exclusoes_base = resultado["exclusoes_base"]
            registro.base_pis = resultado["base_pis"]
            registro.aliquota_pis = resultado["aliquota_pis"]
            registro.debito_pis = resultado["debito_pis"]
            registro.credito_pis = resultado["credito_pis"]
            registro.saldo_pis = resultado["saldo_pis"]
            registro.base_cofins = resultado["base_cofins"]
            registro.aliquota_cofins = resultado["aliquota_cofins"]
            registro.debito_cofins = resultado["debito_cofins"]
            registro.credito_cofins = resultado["credito_cofins"]
            registro.saldo_cofins = resultado["saldo_cofins"]

            db.commit()
            db.refresh(registro)

            return {
                "salvo": True,
                "existente": existente,
                "id": registro.id,
                "company_id": registro.company_id,
                "competencia": registro.competencia,
                "regime_apuracao": registro.regime_apuracao,
                "saldo_pis": registro.saldo_pis,
                "saldo_cofins": registro.saldo_cofins,
            }

        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
