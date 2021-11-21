from pydantic import BaseSettings


class Settings(BaseSettings):
    user: str
    password: str
    host: str
    database: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
