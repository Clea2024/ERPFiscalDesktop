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


class FiscalDocumentModel(Base):

    __tablename__ = "documentos_fiscais"

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

    chave = Column(
        String(44),
        unique=True,
        nullable=False,
        index=True,
    )

    modelo = Column(
        String(5),
        nullable=False,
    )

    numero = Column(
        String(20),
        nullable=False,
    )

    serie = Column(
        String(10),
        nullable=False,
    )

    data_emissao = Column(
        DateTime,
        nullable=False,
    )

    emitente_cnpj = Column(
        String(14),
        nullable=False,
    )

    emitente_nome = Column(
        String(255),
        nullable=False,
    )

    destinatario_cnpj = Column(
        String(14),
        nullable=False,
    )

    destinatario_nome = Column(
        String(255),
        nullable=False,
    )

    valor_total = Column(
        Numeric(15, 2),
        default=0,
    )

    protocolo = Column(
        String(100),
        default="",
    )

    origem = Column(
        String(30),
        default="MANUAL",
    )

    xml_path = Column(
        String(500),
        default="",
    )

    status = Column(
        String(20),
        default="IMPORTADO",
    )

    created_at = Column(
        DateTime,
        default=datetime.now,
    )

    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )

    empresa = relationship(
        "Company",
        lazy="joined",
    )
    itens = relationship(
    "FiscalItemModel",
    back_populates="documento",
    cascade="all, delete-orphan",
    lazy="selectin",
)