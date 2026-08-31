from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.database import Base


class SefazSyncState(Base):

    __tablename__ = "sefaz_sync_states"

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