from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class FiscalItemModel(Base):

    __tablename__ = "fiscal_items"

    ############################################################
    # CHAVE
    ############################################################

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    fiscal_document_id = Column(
        Integer,
        ForeignKey(
            "documentos_fiscais.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    ############################################################
    # PRODUTO
    ############################################################

    numero_item = Column(Integer)

    codigo = Column(String(60))

    descricao = Column(String(500))

    ean = Column(String(30))

    unidade = Column(String(20))

    quantidade = Column(
        Numeric(18, 4),
        default=0,
    )

    valor_unitario = Column(
        Numeric(18, 6),
        default=0,
    )

    valor_total = Column(
        Numeric(18, 2),
        default=0,
    )

    desconto = Column(
        Numeric(18, 2),
        default=0,
    )

    ############################################################
    # CLASSIFICAÇÃO FISCAL
    ############################################################

    ncm = Column(String(8))

    cest = Column(String(12))

    cfop = Column(String(4))

    ############################################################
    # ICMS
    ############################################################

    origem = Column(String(2))

    cst_icms = Column(String(3))

    csosn = Column(String(3))

    aliquota_icms = Column(
        Numeric(8, 4),
        default=0,
    )

    base_icms = Column(
        Numeric(18, 2),
        default=0,
    )

    valor_icms = Column(
        Numeric(18, 2),
        default=0,
    )

    ############################################################
    # PIS
    ############################################################

    cst_pis = Column(String(3))

    aliquota_pis = Column(
        Numeric(8, 4),
        default=0,
    )

    base_pis = Column(
        Numeric(18, 2),
        default=0,
    )

    valor_pis = Column(
        Numeric(18, 2),
        default=0,
    )

    ############################################################
    # COFINS
    ############################################################

    cst_cofins = Column(String(3))

    aliquota_cofins = Column(
        Numeric(8, 4),
        default=0,
    )

    base_cofins = Column(
        Numeric(18, 2),
        default=0,
    )

    valor_cofins = Column(
        Numeric(18, 2),
        default=0,
    )

    ############################################################
    # REFORMA TRIBUTÁRIA
    ############################################################

    ibs = Column(
        Numeric(18, 2),
        default=0,
    )

    cbs = Column(
        Numeric(18, 2),
        default=0,
    )

    imposto_seletivo = Column(
        Numeric(18, 2),
        default=0,
    )
    ############################################################

    created_at = Column(
        DateTime,
        default=datetime.now,
    )

    ############################################################

    documento = relationship(
        "FiscalDocumentModel",
        back_populates="itens",
    )