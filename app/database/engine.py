"""
Engine principal do ERP Fiscal Desktop
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Config


Config.carregar()

engine = create_engine(
    Config.DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)