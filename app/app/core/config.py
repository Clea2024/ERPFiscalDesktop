"""
Configurações globais do ERP Fiscal Desktop
"""

from pathlib import Path
import os


class Config:

    # ==========================================================
    # CAMINHOS
    # ==========================================================

    BASE_DIR = Path(__file__).resolve().parents[2]

    APP_DIR = BASE_DIR / "app"

    DATABASE_DIR = BASE_DIR / "database"

    XML_DIR = BASE_DIR / "xml"

    REPORTS_DIR = BASE_DIR / "reports"

    LOG_DIR = BASE_DIR / "logs"

    BACKUP_DIR = BASE_DIR / "backups"

    CERTIFICATE_DIR = BASE_DIR / "certificates"

    CACHE_DIR = APP_DIR / "sefaz" / "cache"

    # ==========================================================
    # BANCO
    # ==========================================================

    DATABASE_FILE = DATABASE_DIR / "erp_fiscal.db"

    DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

    # ==========================================================
    # SEFAZ
    # ==========================================================

    AMBIENTE = "producao"

    UF = "CE"

    TIMEOUT = 90

    # ==========================================================
    # LOG
    # ==========================================================

    LOG_LEVEL = "INFO"

    LOG_FILE = LOG_DIR / "erp.log"

    # ==========================================================
    # XML
    # ==========================================================

    XML_ENCODING = "utf-8"

    # ==========================================================
    # AUDITORIA
    # ==========================================================

    SCORE_MAXIMO = 100

    # ==========================================================
    # REFORMA TRIBUTÁRIA
    # ==========================================================

    HABILITAR_IBS = True

    HABILITAR_CBS = True

    HABILITAR_IS = True

    # ==========================================================

    @classmethod
    def criar_diretorios(cls):

        diretorios = [

            cls.DATABASE_DIR,

            cls.XML_DIR,

            cls.REPORTS_DIR,

            cls.LOG_DIR,

            cls.BACKUP_DIR,

            cls.CERTIFICATE_DIR,

            cls.CACHE_DIR,

        ]

        for pasta in diretorios:

            pasta.mkdir(

                parents=True,

                exist_ok=True,

            )

    # ==========================================================

    @classmethod
    def carregar(cls):

        cls.criar_diretorios()

        return cls