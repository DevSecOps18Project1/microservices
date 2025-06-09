"""
Configuration settings for the User Service API
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG: bool = False

    @staticmethod
    def get_url():
        settings = Settings()
        user = settings.POSTGRES_USER
        pw = settings.POSTGRES_PASSWORD
        host = settings.POSTGRES_HOST
        port = settings.POSTGRES_PORT
        db_name = settings.POSTGRES_DB
        url = f'postgresql://{user}:{pw}@{host}:{port}/{db_name}'
        return url
