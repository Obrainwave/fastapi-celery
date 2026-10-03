from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    ENVIRONMENT: str = "development"
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()