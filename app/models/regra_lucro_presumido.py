from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    Numeric,
    String,
)

from app.database.database import Base


class RegraLucroPresumido(Base):

    __tablename__ = "regras_lucro_presumido"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    descricao = Column(
        String(200),
        nullable=False,
    )

    atividade = Column(
        String(100),
        nullable=False,
        index=True,
    )

    percentual_irpj = Column(
        Numeric(10, 4),
        nullable=False,
        default=0,
    )

    percentual_csll = Column(
        Numeric(10, 4),
        nullable=False,
        default=0,
    )

    aliquota_irpj = Column(
        Numeric(10, 4),
        nullable=False,
        default=0,
    )

    aliquota_csll = Column(
        Numeric(10, 4),
        nullable=False,
        default=0,
    )

    limite_adicional_irpj = Column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    aliquota_adicional_irpj = Column(
        Numeric(10, 4),
        nullable=False,
        default=0,
    )

    ativa = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    ############################################################
    # VIGÊNCIA E FAIXAS
    ############################################################

    vigencia_inicio = Column(
        Date,
        nullable=True,
    )

    vigencia_fim = Column(
        Date,
        nullable=True,
    )

    limite_receita = Column(
        Numeric(18, 2),
        nullable=True,
    )

    fator_acrescimo_presuncao = Column(
        Numeric(10, 4),
        nullable=False,
        default=0,
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
