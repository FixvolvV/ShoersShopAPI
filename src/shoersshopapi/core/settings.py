from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

class RunConfig(BaseModel):
    mode: str = "development"

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class MinioConfig(BaseModel):
    endpoint_url: str
    access_key: str
    secret_key: str
    bucket_name: str
    region_name: str = "us-east-1"
    file_size: int = 5 # MB
    allowed_type: list = ["image/png", "image/jpeg", "image/webp"]

class Httpcors(BaseModel):
    urls: list = []

class JWTConfig(BaseModel):
    public: Path
    private: Path
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 5

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db: DatabaseConfig
    minio: MinioConfig
    httpcors: Httpcors = Httpcors()
    jwt: JWTConfig

    model_config = SettingsConfigDict (
        env_file=(BASE_DIR / ".env", BASE_DIR / ".env.template"),
        env_nested_delimiter="__",
        env_prefix="API__",
        case_sensitive=False,
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings() #pyright: ignore