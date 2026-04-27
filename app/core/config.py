from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_USERNAME: str = "admin"
    API_PASSWORD: str = "secret"
    DATABASE_URL: str = "sqlite:///./unbake.db"
    WHISPER_MODEL: str = "large-v2"
    WHISPER_BATCH_SIZE: int = 16

    class Config:
        env_file = ".env"


settings = Settings()
