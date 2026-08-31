from dataclasses import dataclass
from decimal import Decimal


@dataclass
class FiscalItem:

    ############################################################
    # PRODUTO
    ############################################################

    numero_item: int = 0

    codigo: str = ""

    descricao: str = ""

    ean: str = ""

    unidade: str = ""

    quantidade: Decimal = Decimal("0.00")

    valor_unitario: Decimal = Decimal("0.00")

    valor_total: Decimal = Decimal("0.00")

    desconto: Decimal = Decimal("0.00")

    ############################################################
    # CLASSIFICAÇÃO FISCAL
    ############################################################

    ncm: str = ""

    cest: str = ""

    cfop: str = ""

    cest_obrigatorio: bool = False

    ############################################################
    # ICMS
    ############################################################

    origem: str = ""

    cst_icms: str = ""

    csosn: str = ""

    aliquota_icms: Decimal = Decimal("0.00")

    base_icms: Decimal = Decimal("0.00")

    valor_icms: Decimal = Decimal("0.00")

    ############################################################
    # ICMS ST
    ############################################################

    base_st: Decimal = Decimal("0.00")

    valor_st: Decimal = Decimal("0.00")

    ############################################################
    # FCP
    ############################################################

    valor_fcp: Decimal = Decimal("0.00")

    ############################################################
    # PIS
    ############################################################

    cst_pis: str = ""

    aliquota_pis: Decimal = Decimal("0.00")

    base_pis: Decimal = Decimal("0.00")

    valor_pis: Decimal = Decimal("0.00")

    ############################################################
    # COFINS
    ############################################################

    cst_cofins: str = ""

    aliquota_cofins: Decimal = Decimal("0.00")

    base_cofins: Decimal = Decimal("0.00")

    valor_cofins: Decimal = Decimal("0.00")

    ############################################################
    # REFORMA TRIBUTÁRIA
    ############################################################

    ibs: Decimal = Decimal("0.00")

    cbs: Decimal = Decimal("0.00")

    imposto_seletivo: Decimal = Decimal("0.00")