from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.database import Base

class Empresa(Base):

    __tablename__ = "empresas"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    cnpj = Column(
        String(14),
        nullable=False,
        unique=True,
        index=True,
    )

    razao_social = Column(
        String(200),
        nullable=False,
    )

    nome_fantasia = Column(
        String(200),
        nullable=True,
    )

    certificado = Column(
        String(500),
        nullable=True,
    )

    ambiente = Column(
        String(20),
        default="producao",
    )

    ultimo_nsu = Column(
        String(15),
        default="000000000000000",
    )

    ativa = Column(
        Boolean,
        default=True,
    )

    def __repr__(self):

        return f"<Empresa {self.cnpj}>"