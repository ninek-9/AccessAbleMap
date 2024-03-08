import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 5432)


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 5432)


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 5432)
