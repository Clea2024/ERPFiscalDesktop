"""
Logger central do ERP Fiscal Desktop
"""

import logging
from logging.handlers import RotatingFileHandler

from app.core.config import Config


class ERPLogger:

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger:

            return cls._logger

        Config.carregar()

        logger = logging.getLogger("ERPFiscal")

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

        )

        arquivo = RotatingFileHandler(

            Config.LOG_FILE,

            maxBytes=5 * 1024 * 1024,

            backupCount=10,

            encoding="utf-8",

        )

        arquivo.setFormatter(formatter)

        console = logging.StreamHandler()

        console.setFormatter(formatter)

        logger.addHandler(arquivo)

        logger.addHandler(console)

        cls._logger = logger

        return logger