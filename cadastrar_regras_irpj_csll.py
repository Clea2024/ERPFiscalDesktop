from datetime import date
from decimal import Decimal

from app.database.database import get_session
from app.models.regra_lucro_presumido import RegraLucroPresumido

db = get_session()

regras = [
    {
        "descricao": "Comércio e indústria",
        "atividade": "COMERCIO_INDUSTRIA",
        "percentual_irpj": Decimal("0.08"),
        "percentual_csll": Decimal("0.12"),
        "aliquota_irpj": Decimal("0.15"),
        "aliquota_csll": Decimal("0.09"),
        "limite_adicional_irpj": Decimal("60000.00"),
        "aliquota_adicional_irpj": Decimal("0.10"),
        "vigencia_inicio": date(2026, 1, 1),
        "vigencia_fim": None,
        "limite_receita": None,
        "fator_acrescimo_presuncao": Decimal("0.00"),
        "ativa": True,
    },
    {
        "descricao": "Serviços em geral",
        "atividade": "SERVICOS_GERAIS",
        "percentual_irpj": Decimal("0.32"),
        "percentual_csll": Decimal("0.32"),
        "aliquota_irpj": Decimal("0.15"),
        "aliquota_csll": Decimal("0.09"),
        "limite_adicional_irpj": Decimal("60000.00"),
        "aliquota_adicional_irpj": Decimal("0.10"),
        "vigencia_inicio": date(2026, 1, 1),
        "vigencia_fim": None,
        "limite_receita": None,
        "fator_acrescimo_presuncao": Decimal("0.00"),
        "ativa": True,
    },
]

for dados in regras:

    existente = (
        db.query(RegraLucroPresumido)
        .filter(
            RegraLucroPresumido.atividade
            == dados["atividade"]
        )
        .first()
    )

    if existente is None:

        db.add(
            RegraLucroPresumido(
                **dados
            )
        )

        print(
            "CRIADA:",
            dados["atividade"]
        )

    else:

        print(
            "JÁ EXISTE:",
            dados["atividade"]
        )

db.commit()
db.close()
