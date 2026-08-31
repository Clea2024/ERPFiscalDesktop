from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from app.dfe.document_type import DFeType


@dataclass
class DFeDocument:

    tipo: DFeType

    chave: str = ""
    numero: str = ""
    serie: str = ""
    modelo: str = ""

    emitente_documento: str = ""
    emitente_nome: str = ""

    destinatario_documento: str = ""
    destinatario_nome: str = ""

    data_emissao: Optional[datetime] = None

    valor_total: Decimal = Decimal("0")

    xml_path: str = ""
    xml_content: str = ""

    nsu: str = ""
    schema: str = ""

    origem: str = ""
    status: str = ""
    protocolo: str = ""