from decimal import Decimal, ROUND_HALF_UP


class PisCofinsService:
    ZERO = Decimal("0.00")

    ALIQUOTAS_PADRAO = {
        "CUMULATIVO": {
            "pis": Decimal("0.0065"),
            "cofins": Decimal("0.03"),
        },
        "NAO_CUMULATIVO": {
            "pis": Decimal("0.0165"),
            "cofins": Decimal("0.076"),
        },
    }

    @staticmethod
    def decimal(valor):
        return Decimal(str(valor or 0))

    @staticmethod
    def arredondar(valor):
        return Decimal(valor).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    def calcular(
        self,
        receita_tributavel,
        regime_apuracao,
        exclusoes_base=0,
        credito_pis=0,
        credito_cofins=0,
        aliquota_pis=None,
        aliquota_cofins=None,
    ):
        regime = str(regime_apuracao or "").strip().upper()

        if regime not in self.ALIQUOTAS_PADRAO:
            raise ValueError("Regime de PIS/COFINS inválido.")

        receita = self.decimal(receita_tributavel)
        exclusoes = self.decimal(exclusoes_base)
        base = max(self.ZERO, receita - exclusoes)

        padrao = self.ALIQUOTAS_PADRAO[regime]

        aliq_pis = (
            self.decimal(aliquota_pis)
            if aliquota_pis is not None
            else padrao["pis"]
        )
        aliq_cofins = (
            self.decimal(aliquota_cofins)
            if aliquota_cofins is not None
            else padrao["cofins"]
        )

        debito_pis = base * aliq_pis
        debito_cofins = base * aliq_cofins

        if regime == "CUMULATIVO":
            credito_pis = self.ZERO
            credito_cofins = self.ZERO
        else:
            credito_pis = max(self.ZERO, self.decimal(credito_pis))
            credito_cofins = max(self.ZERO, self.decimal(credito_cofins))

        saldo_pis = max(self.ZERO, debito_pis - credito_pis)
        saldo_cofins = max(self.ZERO, debito_cofins - credito_cofins)

        return {
            "regime_apuracao": regime,
            "receita_tributavel": self.arredondar(receita),
            "exclusoes_base": self.arredondar(exclusoes),
            "base_pis": self.arredondar(base),
            "aliquota_pis": aliq_pis,
            "debito_pis": self.arredondar(debito_pis),
            "credito_pis": self.arredondar(credito_pis),
            "saldo_pis": self.arredondar(saldo_pis),
            "base_cofins": self.arredondar(base),
            "aliquota_cofins": aliq_cofins,
            "debito_cofins": self.arredondar(debito_cofins),
            "credito_cofins": self.arredondar(credito_cofins),
            "saldo_cofins": self.arredondar(saldo_cofins),
        }
