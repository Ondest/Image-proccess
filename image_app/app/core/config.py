from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class JWT(BaseModel):
    algorithm: str = "RS256"
    public_key: Path = BASE_DIR / "certs" / "public.pem"
    private_key: Path = BASE_DIR / "certs" / "private.pem"
    expire: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_PORT: int
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB: str

    REDIS_HOST: str
    REDIS_PORT: int

    KAFKA_HOST: str
    KAFKA_PORT: int
    KAFKA_GROUP_ID: str
    KAFKA_REPLY_TOPIC: str
    KAFKA_REQUEST_TOPIC: str

    ALLOWED_CONTENT_TYPES: list[str] = ["image/jpeg", "image/png", "image/gif"]
    MAX_FILE_SIZE: int

    LOGGING_LEVEL: str

    JWT: ClassVar = JWT()

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def test_db_url(self):
        return self.db_url.replace(self.DB_NAME, self.TEST_DB)

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def kafka_url(self):
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"


settings = Settings()  # type: ignore
