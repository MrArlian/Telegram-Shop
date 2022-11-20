from pydantic import BaseSettings


class Settings(BaseSettings):
    TelegramToken: str

    DatabaseUrl: str

    Host: str
    Port: int
    Password: str

    ShopId: str
    ApiKey: str

    class Config:
        env_file = 'static/config.cfg'
        env_file_encoding = 'utf-8'

settings = Settings()
