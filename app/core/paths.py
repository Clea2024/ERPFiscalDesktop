"""
Gerenciador de caminhos do ERP Fiscal Desktop
"""

from pathlib import Path
from app.core.config import Config


class Paths:

    BASE = Config.BASE_DIR

    APP = Config.APP_DIR

    DATABASE = Config.DATABASE_DIR

    XML = Config.XML_DIR

    REPORTS = Config.REPORTS_DIR

    LOGS = Config.LOG_DIR

    BACKUPS = Config.BACKUP_DIR

    CERTIFICATES = Config.CERTIFICATE_DIR

    CACHE = Config.CACHE_DIR

    @classmethod
    def criar_estrutura(cls):

        pastas = [

            cls.DATABASE,

            cls.XML,

            cls.REPORTS,

            cls.LOGS,

            cls.BACKUPS,

            cls.CERTIFICATES,

            cls.CACHE,

        ]

        for pasta in pastas:

            pasta.mkdir(

                parents=True,

                exist_ok=True,

            )

    @classmethod
    def mostrar(cls):

        print("=" * 60)

        print("ESTRUTURA DO ERP")

        print("=" * 60)

        print("BASE........:", cls.BASE)

        print("APP.........:", cls.APP)

        print("DATABASE....:", cls.DATABASE)

        print("XML.........:", cls.XML)

        print("REPORTS.....:", cls.REPORTS)

        print("LOGS........:", cls.LOGS)

        print("BACKUPS.....:", cls.BACKUPS)

        print("CERTIFICATES:", cls.CERTIFICATES)

        print("CACHE.......:", cls.CACHE)