from decimal import Decimal

from app.services.pis_cofins_service import PisCofinsService


def test_cumulativo():
    service = PisCofinsService()
    resultado = service.calcular(
        receita_tributavel=100000,
        regime_apuracao="CUMULATIVO",
    )

    assert resultado["debito_pis"] == Decimal("650.00")
    assert resultado["debito_cofins"] == Decimal("3000.00")
    assert resultado["saldo_pis"] == Decimal("650.00")
    assert resultado["saldo_cofins"] == Decimal("3000.00")


def test_nao_cumulativo():
    service = PisCofinsService()
    resultado = service.calcular(
        receita_tributavel=100000,
        regime_apuracao="NAO_CUMULATIVO",
        credito_pis=500,
        credito_cofins=2000,
    )

    assert resultado["debito_pis"] == Decimal("1650.00")
    assert resultado["debito_cofins"] == Decimal("7600.00")
    assert resultado["saldo_pis"] == Decimal("1150.00")
    assert resultado["saldo_cofins"] == Decimal("5600.00")
