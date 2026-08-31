from datetime import date

from app.services.lucro_presumido_service import (
    LucroPresumidoService,
)
from app.services.regra_tributaria_service import (
    RegraTributariaService,
)


class ApuracaoLucroPresumidoService:

    def __init__(self):

        self.regras = RegraTributariaService()
        self.calculadora = LucroPresumidoService()

    @staticmethod
    def identificar_trimestre(
        mes,
        ano,
    ):

        mes = int(mes)
        ano = int(ano)

        if mes in (1, 2, 3):
            trimestre = 1
            meses = (1, 2, 3)

        elif mes in (4, 5, 6):
            trimestre = 2
            meses = (4, 5, 6)

        elif mes in (7, 8, 9):
            trimestre = 3
            meses = (7, 8, 9)

        elif mes in (10, 11, 12):
            trimestre = 4
            meses = (10, 11, 12)

        else:
            raise ValueError(
                "Mês inválido."
            )

        return {
            "ano": ano,
            "trimestre": trimestre,
            "meses": meses,
            "competencias": [
                f"{ano}-{m:02d}"
                for m in meses
            ],
        }

    @staticmethod
    def data_final_trimestre(
        trimestre,
        ano,
    ):

        datas = {
            1: date(ano, 3, 31),
            2: date(ano, 6, 30),
            3: date(ano, 9, 30),
            4: date(ano, 12, 31),
        }

        return datas[
            trimestre
        ]

    def apurar(
        self,
        atividade,
        receita,
        data_referencia=None,
    ):

        regra = self.regras.buscar_regra(
            atividade=atividade,
            data_referencia=data_referencia,
            receita=receita,
        )

        if not regra.get(
            "encontrada"
        ):

            return {
                "apurado": False,
                "mensagem": regra.get(
                    "mensagem",
                    "Regra tributária não encontrada.",
                ),
            }

        resultado = self.calculadora.calcular(
            receita_bruta=receita,
            percentual_presuncao_irpj=(
                regra["percentual_irpj"]
            ),
            percentual_presuncao_csll=(
                regra["percentual_csll"]
            ),
            aliquota_irpj=(
                regra["aliquota_irpj"]
            ),
            aliquota_csll=(
                regra["aliquota_csll"]
            ),
            limite_adicional_irpj=(
                regra[
                    "limite_adicional_irpj"
                ]
            ),
            aliquota_adicional_irpj=(
                regra[
                    "aliquota_adicional_irpj"
                ]
            ),
        )

        resultado["apurado"] = True
        resultado["atividade"] = atividade
        resultado["regra_id"] = regra["id"]
        resultado["regra_descricao"] = (
            regra["descricao"]
        )

        return resultado