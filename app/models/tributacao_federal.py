from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class TributacaoFederal(Base):

    __tablename__ = "tributacao_federal"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    company_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False,
        index=True,
    )

    competencia = Column(
        String(7),
        nullable=False,
        index=True,
    )

    regime = Column(
        String(50),
        nullable=False,
    )

    receita_bruta = Column(
        Numeric(18, 2),
        default=0,
    )

    ############################################################
    # IRPJ
    ############################################################

    base_irpj = Column(
        Numeric(18, 2),
        default=0,
    )

    aliquota_irpj = Column(
        Numeric(10, 4),
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

    ############################################################
    # CSLL
    ############################################################

    base_csll = Column(
        Numeric(18, 2),
        default=0,
    )

    aliquota_csll = Column(
        Numeric(10, 4),
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

    ############################################################
    # RECOLHIMENTO
    ############################################################

    vencimento_irpj = Column(
        Date,
        nullable=True,
    )

    vencimento_csll = Column(
        Date,
        nullable=True,
    )

    darf_irpj = Column(
        String(50),
        default="",
    )

    darf_csll = Column(
        String(50),
        default="",
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

    empresa = relationship(
        "Company",
        lazy="joined",
    )