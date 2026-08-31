from app.core.logger import ERPLogger

logger = ERPLogger.get_logger()

logger.info("ERP iniciado.")

logger.warning("Teste de aviso.")

logger.error("Teste de erro.")

print("Logger funcionando.")