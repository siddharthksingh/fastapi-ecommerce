import configparser

config = configparser.ConfigParser()

config.read("settings.ini")

MONGO_URI = config.get("database", "MONGO_URI", fallback="mongodb://localhost:27017")
DB_NAME = config.get("database", "DB_NAME", fallback="ecommerce_db")
JWT_SECRET = config.get("security", "JWT_SECRET", fallback="your_secret_key")
