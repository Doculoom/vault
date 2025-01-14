import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "doculoom-446020")
    EMBEDDING_MODEL_ID: str = "models/text-embedding-004"
    MODEL_SAVE_PATH: str = "./app/utils/models"
    DB_NAME: str = os.getenv("DB_NAME", "vault")

    class Config:
        env_file = ".env"


settings = Settings()
