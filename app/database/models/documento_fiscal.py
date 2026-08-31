from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class DocumentoFiscal(Base):

    __tablename__ = "documentos_fiscais"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    empresa_id = Column(
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

    numero = Column(
        String(20),
    )

    serie = Column(
        String(10),
    )

    modelo = Column(
        String(5),
    )

    tipo = Column(
        String(10),
    )

    data_emissao = Column(
        DateTime,
    )

    valor_total = Column(
        Numeric(15,2),
    )

    xml_path = Column(
        String(500),
    )

    empresa = relationship(
        "Empresa",
    )