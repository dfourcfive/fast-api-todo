import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME : str = os.getenv("PROJECT_NAME","")
    PROJECT_VERSION = "1.0.0"

    POSTGRES_USER : str = os.environ.get("POSTGRES_USER","")
    POSTGRES_PASSWORD : str= os.environ.get("POSTGRES_PASSWORD","")
    POSTGRES_SERVER : str = os.environ.get("POSTGRES_SERVER","localhost")
    POSTGRES_PORT  = os.environ.get("POSTGRES_PORT",5432) # default postgres port is 5432
    POSTGRES_DB : str = os.environ.get("POSTGRES_DB","tdd")
    DATABASE_URL : str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SECRET_KEY : str = os.environ.get("SECRET_KEY","secret_key_fallback_value")
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES",60)  # in mins

settings = Settings()
