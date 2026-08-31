from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_PATH = DATABASE_DIR / "sistema_fiscal.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


def get_session():
    return SessionLocal()


def create_database():

    from app.models.user import User
    from app.models.company import Company
    from app.models.certificate import Certificate
    from app.models.fiscal_document import FiscalDocumentModel
    from app.models.dfe_sync_state import DFeSyncState
    from app.models.tributacao_federal import TributacaoFederal
    from app.models.regra_lucro_presumido import RegraLucroPresumido
    from app.models.tributacao_lucro_real import TributacaoLucroReal
    from app.models.tributacao_pis_cofins import TributacaoPisCofins
    

    Base.metadata.create_all(
        bind=engine
    )