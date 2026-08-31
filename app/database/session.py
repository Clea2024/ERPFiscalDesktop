"""
Gerenciamento das sessões do banco
"""

from app.database.engine import SessionLocal


class DatabaseSession:

    @staticmethod
    def get():

        return SessionLocal()