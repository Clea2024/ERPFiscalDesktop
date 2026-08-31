from app.core.config import Config

Config.carregar()

print(Config.BASE_DIR)

print(Config.DATABASE_FILE)

print(Config.XML_DIR)

print(Config.LOG_FILE)