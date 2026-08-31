from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class XMLDocumento(Base):

    __tablename__ = "xml_documentos"

    id = Column(
        Integer,
        primary_key=True,
    )

    documento_id = Column(
        Integer,
        ForeignKey(
            "documentos_fiscais.id"
        ),
    )

    xml = Column(
        Text,
    )

    documento = relationship(
        "DocumentoFiscal",
    )