from decimal import Decimal, ROUND_HALF_UP


class LucroRealService:

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
        custos,
        despesas_dedutiveis,
        outras_receitas=0,
        adicoes=0,
        exclusoes=0,
        compensacoes=0,
        meses_periodo=3,
        aliquota_irpj=Decimal("0.15"),
        aliquota_adicional_irpj=Decimal("0.10"),
        aliquota_csll=Decimal("0.09"),
    ):

        receita = self.decimal(
            receita_bruta
        )

        custos = self.decimal(
            custos
        )

        despesas = self.decimal(
            despesas_dedutiveis
        )

        outras_receitas = self.decimal(
            outras_receitas
        )

        adicoes = self.decimal(
            adicoes
        )

        exclusoes = self.decimal(
            exclusoes
        )

        compensacoes = self.decimal(
            compensacoes
        )

        meses_periodo = int(
            meses_periodo
        )

        lucro_contabil = (
            receita
            + outras_receitas
            - custos
            - despesas
        )

        lucro_ajustado = (
            lucro_contabil
            + adicoes
            - exclusoes
        )

        base_irpj = max(
            self.ZERO,
            lucro_ajustado
            - compensacoes
        )

        base_csll = max(
            self.ZERO,
            lucro_ajustado
            - compensacoes
        )

        irpj_normal = (
            base_irpj
            * self.decimal(
                aliquota_irpj
            )
        )

        limite_adicional = (
            Decimal("20000.00")
            * meses_periodo
        )

        excedente = max(
            self.ZERO,
            base_irpj
            - limite_adicional
        )

        adicional_irpj = (
            excedente
            * self.decimal(
                aliquota_adicional_irpj
            )
        )

        valor_irpj = (
            irpj_normal
            + adicional_irpj
        )

        valor_csll = (
            base_csll
            * self.decimal(
                aliquota_csll
            )
        )

        return {
            "receita_bruta": self.arredondar(
                receita
            ),
            "custos": self.arredondar(
                custos
            ),
            "despesas_dedutiveis": self.arredondar(
                despesas
            ),
            "outras_receitas": self.arredondar(
                outras_receitas
            ),
            "lucro_contabil": self.arredondar(
                lucro_contabil
            ),
            "adicoes": self.arredondar(
                adicoes
            ),
            "exclusoes": self.arredondar(
                exclusoes
            ),
            "compensacoes": self.arredondar(
                compensacoes
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
                valor_irpj
            ),
            "base_csll": self.arredondar(
                base_csll
            ),
            "valor_csll": self.arredondar(
                valor_csll
            ),
        }