from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AuditResult:

    regra: str

    severidade: str

    mensagem: str

    item: Optional[int] = None

    codigo: str = ""

    valor_encontrado: str = ""

    valor_correto: str = ""

    fundamento_legal: str = ""

    sugestao: str = ""

    campo: str = ""

    xml: str = ""

    created_at: datetime = datetime.now()

    @property
    def sucesso(self):

        return self.severidade == "SUCESSO"

    @property
    def info(self):

        return self.severidade == "INFO"

    @property
    def alerta(self):

        return self.severidade == "ALERTA"

    @property
    def erro(self):

        return self.severidade == "ERRO"

    @property
    def critico(self):

        return self.severidade == "CRITICO"

    def to_dict(self):

        return {
            "regra": self.regra,
            "severidade": self.severidade,
            "mensagem": self.mensagem,
            "item": self.item,
            "codigo": self.codigo,
            "valor_encontrado": self.valor_encontrado,
            "valor_correto": self.valor_correto,
            "fundamento_legal": self.fundamento_legal,
            "sugestao": self.sugestao,
            "campo": self.campo,
            "xml": self.xml,
            "created_at": self.created_at,
        }

    def __str__(self):

        texto = (
            f"[{self.severidade}] "
            f"{self.regra} - "
            f"{self.mensagem}"
        )

        if self.item is not None:

            texto += f" (Item {self.item})"

        return texto