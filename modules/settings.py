import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    TelegramToken: str

    DatabaseUrl: str

    Host: str
    Port: int
    Password: str

    ShopId: str
    ApiKey: str
    Secret: str

    Admin: int

    class Config:
        env_file = os.path.join(os.path.abspath('.'), 'static', 'config.cfg')
        env_file_encoding = 'utf-8'

settings = Settings()
