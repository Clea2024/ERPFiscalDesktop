from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Severity(Enum):

    INFO = "INFO"

    BAIXA = "BAIXA"

    MEDIA = "MEDIA"

    ALTA = "ALTA"

    CRITICA = "CRITICA"


@dataclass
class AuditResult:

    documento: str = ""

    regra: str = ""

    descricao: str = ""

    severidade: Severity = Severity.INFO

    legislacao: str = ""

    sugestao: str = ""

    aprovado: bool = True

    data_auditoria: datetime | None = None

    valor_envolvido: float = 0.0

    observacao: str = ""
    