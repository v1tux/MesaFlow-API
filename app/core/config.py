from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "MesaFlow API"
    SECRET_KEY: str = "troque-essa-chave-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    DATABASE_URL: str = "sqlite:///./mesaflow.db"

    class Config:
        env_file = ".env"


settings = Settings()
