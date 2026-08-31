"""
Configurações globais do ERP Fiscal Desktop
"""

from pathlib import Path


class Config:

    # Diretório raiz do projeto
    BASE_DIR = Path(__file__).resolve().parents[2]

    # Pastas principais
    APP_DIR = BASE_DIR / "app"
    DATABASE_DIR = BASE_DIR / "database"
    XML_DIR = BASE_DIR / "xml"
    REPORTS_DIR = BASE_DIR / "reports"
    LOG_DIR = BASE_DIR / "logs"
    LOG_FILE = LOG_DIR / "erp.log"
    BACKUP_DIR = BASE_DIR / "backups"
    CERTIFICATE_DIR = BASE_DIR / "certificates"
    CACHE_DIR = APP_DIR / "sefaz" / "cache"

    # Banco de dados
    DATABASE_FILE = DATABASE_DIR / "erp_fiscal.db"
    DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

    # Configurações da SEFAZ
    UF = "CE"
    AMBIENTE = "producao"
    TIMEOUT = 90

    @classmethod
    def criar_diretorios(cls):

        diretorios = [
            cls.DATABASE_DIR,
            cls.XML_DIR,
            cls.REPORTS_DIR,
            cls.LOG_DIR,
            cls.BACKUP_DIR,
            cls.CERTIFICATE_DIR,
        ]

        for pasta in diretorios:
            pasta.mkdir(
                parents=True,
                exist_ok=True,
            )

    @classmethod
    def carregar(cls):
        cls.criar_diretorios()
        return cls