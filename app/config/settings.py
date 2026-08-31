from pathlib import Path


class Settings:

    APP_NAME = "ERP Fiscal Desktop CE"

    VERSION = "0.1.0"

    ROOT = Path(__file__).resolve().parents[2]

    DATABASE = ROOT / "database" / "erp_fiscal.db"

    XML_FOLDER = ROOT / "xml"

    REPORT_FOLDER = ROOT / "reports"

    LOG_FOLDER = ROOT / "logs"

    CERTIFICATE_FOLDER = ROOT / "certificates"