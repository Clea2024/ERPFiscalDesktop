from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from app.database.database import Base
from app.models.company import Company


class Certificate(Base):

    __tablename__ = "certificados"

    id = Column(Integer, primary_key=True)

    company_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False,
    )

    descricao = Column(
        String(150),
        nullable=False,
    )

    arquivo = Column(
        String(500),
        nullable=False,
    )

    senha = Column(
        String(255),
        nullable=False,
    )

    validade = Column(DateTime)

    emissor = Column(String(200))

    serial = Column(String(200))

    ativo = Column(
        String(1),
        default="S",
    )

    empresa = relationship(
        "Company",
        lazy="joined",
    )

    def __repr__(self):

        return (
            f"<Certificate(id={self.id}, descricao='{self.descricao}')>"
        )