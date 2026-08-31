from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from app.database.database import Base


class TributacaoLucroReal(Base):

    __tablename__ = "tributacao_lucro_real"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    company_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False,
    )

    periodo = Column(
        String(20),
        nullable=False,
    )

    forma_apuracao = Column(
        String(30),
        nullable=False,
    )

    receita_bruta = Column(
        Numeric(18, 2),
        default=0,
    )

    custos = Column(
        Numeric(18, 2),
        default=0,
    )

    despesas_dedutiveis = Column(
        Numeric(18, 2),
        default=0,
    )

    outras_receitas = Column(
        Numeric(18, 2),
        default=0,
    )

    lucro_contabil = Column(
        Numeric(18, 2),
        default=0,
    )

    adicoes = Column(
        Numeric(18, 2),
        default=0,
    )

    exclusoes = Column(
        Numeric(18, 2),
        default=0,
    )

    compensacoes = Column(
        Numeric(18, 2),
        default=0,
    )

    base_irpj = Column(
        Numeric(18, 2),
        default=0,
    )

    adicional_irpj = Column(
        Numeric(18, 2),
        default=0,
    )

    valor_irpj = Column(
        Numeric(18, 2),
        default=0,
    )

    irpj_recolhido = Column(
        Numeric(18, 2),
        default=0,
    )

    base_csll = Column(
        Numeric(18, 2),
        default=0,
    )

    valor_csll = Column(
        Numeric(18, 2),
        default=0,
    )

    csll_recolhida = Column(
        Numeric(18, 2),
        default=0,
    )

    status_irpj = Column(
        String(20),
        default="PENDENTE",
    )

    status_csll = Column(
        String(20),
        default="PENDENTE",
    )

    criado_em = Column(
        DateTime,
        default=datetime.now,
    )

    atualizado_em = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )