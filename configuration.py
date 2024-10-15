import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False

class LocalConfig(Config):
    DEBUG = True
    BASE_URL = "http://localhost:5000"
    SDESK_API_KEY = os.getenv("SDESK_API_KEY")

class DevConfig(Config):
    DEBUG = True
    BASE_URL = "https://dev.sdesk.co.uk"
    SDESK_API_KEY = os.getenv("SDESK_API_KEY")

class ProdConfig(Config):
    DEBUG = False
    BASE_URL = "http://prod.example.com"
    SDESK_API_KEY = os.getenv("SDESK_API_KEY")

# Get the appropriate configuration based on the environment
def get_config():
    env = os.getenv("FLASK_ENV")
    if env == "local":
        return LocalConfig()
    elif env == "development":
        return DevConfig()
    elif env == "production":
        return ProdConfig()
    else:
        raise ValueError("Invalid FLASK_ENV value. Choose from 'local', 'development', or 'production'.")
