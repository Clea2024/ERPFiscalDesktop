"""
Exceções do ERP Fiscal Desktop
"""


class ERPException(Exception):
    """Exceção base do sistema."""
    pass


class ConfigException(ERPException):
    pass


class DatabaseException(ERPException):
    pass


class SefazException(ERPException):
    pass


class CertificateException(SefazException):
    pass


class XMLException(ERPException):
    pass


class AuditoriaException(ERPException):
    pass


class DashboardException(ERPException):
    pass