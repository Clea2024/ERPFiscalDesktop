from decimal import Decimal, ROUND_HALF_UP


class LucroPresumidoService:

    ZERO = Decimal("0.00")

    @staticmethod
    def decimal(valor):
        return Decimal(
            str(valor or 0)
        )

    @staticmethod
    def arredondar(valor):
        return Decimal(valor).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    def calcular(
        self,
        receita_bruta,
        percentual_presuncao_irpj,
        percentual_presuncao_csll,
        aliquota_irpj,
        aliquota_csll,
        limite_adicional_irpj=0,
        aliquota_adicional_irpj=0,
    ):

        receita = self.decimal(
            receita_bruta
        )

        perc_irpj = self.decimal(
            percentual_presuncao_irpj
        )

        perc_csll = self.decimal(
            percentual_presuncao_csll
        )

        aliq_irpj = self.decimal(
            aliquota_irpj
        )

        aliq_csll = self.decimal(
            aliquota_csll
        )

        limite_adicional = self.decimal(
            limite_adicional_irpj
        )

        aliq_adicional = self.decimal(
            aliquota_adicional_irpj
        )

        base_irpj = (
            receita * perc_irpj
        )

        base_csll = (
            receita * perc_csll
        )

        irpj_normal = (
            base_irpj * aliq_irpj
        )

        csll = (
            base_csll * aliq_csll
        )

        excedente = max(
            self.ZERO,
            base_irpj - limite_adicional,
        )

        adicional_irpj = (
            excedente * aliq_adicional
        )

        total_irpj = (
            irpj_normal
            + adicional_irpj
        )

        return {
            "receita_bruta": self.arredondar(
                receita
            ),
            "base_irpj": self.arredondar(
                base_irpj
            ),
            "irpj_normal": self.arredondar(
                irpj_normal
            ),
            "adicional_irpj": self.arredondar(
                adicional_irpj
            ),
            "valor_irpj": self.arredondar(
                total_irpj
            ),
            "base_csll": self.arredondar(
                base_csll
            ),
            "valor_csll": self.arredondar(
                csll
            ),
        }
