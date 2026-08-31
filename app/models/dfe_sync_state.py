from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from app.database.database import Base


class DFeSyncState(Base):

    __tablename__ = "dfe_sync_states"

    __table_args__ = (
        UniqueConstraint(
            "cnpj",
            "tipo",
            name="uq_dfe_sync_cnpj_tipo",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    cnpj = Column(
        String(14),
        nullable=False,
        index=True,
    )

    tipo = Column(
        String(20),
        nullable=False,
        index=True,
    )

    ultimo_nsu = Column(
        String(15),
        nullable=False,
        default="000000000000000",
    )

    max_nsu = Column(
        String(15),
        nullable=False,
        default="000000000000000",
    )

    ultimo_cstat = Column(
        String(10),
        nullable=True,
    )

    ultimo_motivo = Column(
        String(500),
        nullable=True,
    )

    ultima_consulta = Column(
        DateTime,
        nullable=True,
    )

    bloqueado_ate = Column(
        DateTime,
        nullable=True,
    )

    atualizado_em = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )