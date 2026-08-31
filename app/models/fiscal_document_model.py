from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import Text
from sqlalchemy import String

from app.database.base import Base


class FiscalDocumentModel(Base):

    __tablename__ = "fiscal_documents"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    chave = Column(
        String(44),
        unique=True,
        nullable=False,
        index=True,
    )

    modelo = Column(
        String(2),
        nullable=False,
    )

    numero = Column(
        String(20),
        nullable=False,
    )

    serie = Column(
        String(10),
        nullable=True,
    )

    data_emissao = Column(
        DateTime,
        nullable=True,
    )

    emitente_cnpj = Column(
        String(14),
        nullable=False,
        index=True,
    )

    emitente_nome = Column(
        String(255),
        nullable=False,
    )

    destinatario_cnpj = Column(
        String(14),
        nullable=True,
        index=True,
    )

    destinatario_nome = Column(
        String(255),
        nullable=True,
    )

    valor_total = Column(
        Numeric(18, 2),
        nullable=False,
    )

    protocolo = Column(
        String(30),
        nullable=True,
    )

    origem = Column(
        String(30),
        nullable=True,
    )

    empresa_id = Column(
        Integer,
        nullable=True,
        index=True,
    )

    itens = relationship(
    "FiscalItemModel",
    back_populates="documento",
    cascade="all, delete-orphan",
    lazy="selectin",
)

xml_path = Column(
    String(500),
    nullable=True,
)

xml = Column(
    Text,
    nullable=False,
)