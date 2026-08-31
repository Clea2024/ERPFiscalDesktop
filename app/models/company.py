from sqlalchemy import Column, Integer, String

from app.database.database import Base

class Company(Base):

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True)

    razao_social = Column(String(200), nullable=False)

    nome_fantasia = Column(String(200))

    cnpj = Column(String(18), unique=True, nullable=False)

    inscricao_estadual = Column(String(30))

    inscricao_municipal = Column(String(30))

    regime = Column(String(50))

    certificado = Column(String(255))

    def __str__(self):
        return self.razao_social