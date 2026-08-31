from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String

from app.database.database import Base


class TributacaoPisCofins(Base):
    __tablename__ = "tributacao_pis_cofins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("empresas.id"), nullable=False, index=True)
    competencia = Column(String(7), nullable=False, index=True)
    regime_apuracao = Column(String(30), nullable=False)

    receita_tributavel = Column(Numeric(18, 2), default=0)
    exclusoes_base = Column(Numeric(18, 2), default=0)

    base_pis = Column(Numeric(18, 2), default=0)
    aliquota_pis = Column(Numeric(10, 6), default=0)
    debito_pis = Column(Numeric(18, 2), default=0)
    credito_pis = Column(Numeric(18, 2), default=0)
    pis_recolhido = Column(Numeric(18, 2), default=0)
    saldo_pis = Column(Numeric(18, 2), default=0)

    base_cofins = Column(Numeric(18, 2), default=0)
    aliquota_cofins = Column(Numeric(10, 6), default=0)
    debito_cofins = Column(Numeric(18, 2), default=0)
    credito_cofins = Column(Numeric(18, 2), default=0)
    cofins_recolhida = Column(Numeric(18, 2), default=0)
    saldo_cofins = Column(Numeric(18, 2), default=0)

    status_pis = Column(String(20), default="PENDENTE")
    status_cofins = Column(String(20), default="PENDENTE")

    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)
