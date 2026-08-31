from sqlalchemy import Boolean, Column, Integer, String

from app.database.database import Base

class User(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)

    nome = Column(String(120), nullable=False)

    login = Column(String(80), unique=True, nullable=False)

    senha = Column(String(255), nullable=False)

    email = Column(String(120))

    administrador = Column(Boolean, default=False)

    ativo = Column(Boolean, default=True)