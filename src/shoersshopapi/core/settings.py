from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class RunConfig(BaseModel):
    mode: str = "development"

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class Settings(BaseSettings):
    
    config = SettingsConfigDict (
        env_file=(".env", ".env.template"),
        env_nested_delimiter="__",
        env_prefix="API_",
        case_sensitive=False,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig() #pyright: ignore

settings = Settings()