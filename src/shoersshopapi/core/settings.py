from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class RunConfig(BaseModel):
    mode: str = "development"

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class Httpcors(BaseModel):
    urls: list = []

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db: DatabaseConfig
    httpcors: Httpcors = Httpcors()

    model_config = SettingsConfigDict (
        env_file=(BASE_DIR / ".env", BASE_DIR / ".env.template"),
        env_nested_delimiter="__",
        env_prefix="API__",
        case_sensitive=False,
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings() #pyright: ignore