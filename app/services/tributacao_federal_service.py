from decimal import Decimal


class TributacaoFederalService:

    def calcular_saldo(
        self,
        valor_apurado,
        valor_recolhido,
    ):

        apurado = Decimal(
            str(valor_apurado or 0)
        )

        recolhido = Decimal(
            str(valor_recolhido or 0)
        )

        saldo = apurado - recolhido

        if saldo < 0:
            saldo = Decimal("0")

        return saldo

    def status_recolhimento(
        self,
        valor_apurado,
        valor_recolhido,
    ):

        apurado = Decimal(
            str(valor_apurado or 0)
        )

        recolhido = Decimal(
            str(valor_recolhido or 0)
        )

        if apurado <= 0:
            return "SEM VALOR"

        if recolhido >= apurado:
            return "PAGO"

        if recolhido > 0:
            return "PARCIAL"

        return "PENDENTE"
