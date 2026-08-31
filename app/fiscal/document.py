from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.fiscal.item import FiscalItem


@dataclass
class FiscalDocument:

    ############################################################
    # IDENTIFICAÇÃO
    ############################################################

    chave: str = ""

    modelo: str = ""

    numero: str = ""

    serie: str = ""

    data_emissao: datetime | None = None

    ############################################################
    # EMITENTE
    ############################################################

    emitente_cnpj: str = ""

    emitente_nome: str = ""

    ############################################################
    # DESTINATÁRIO
    ############################################################

    destinatario_cnpj: str = ""

    destinatario_nome: str = ""

    ############################################################
    # TOTAIS
    ############################################################

    valor_total: Decimal = Decimal("0.00")

    ############################################################
    # CONTROLE
    ############################################################

    protocolo: str = ""

    xml: str = ""

    xml_path: str = ""

    origem: str = ""

    empresa_id: int | None = None

    ############################################################
    # ITENS DA NF-e
    ############################################################

    itens: list[FiscalItem] = field(
        default_factory=list
    )