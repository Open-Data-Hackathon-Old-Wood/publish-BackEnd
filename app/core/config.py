## app/core/config.py
from pydantic import BaseModel
import os
from typing import List

class Settings(BaseModel):
    # Database (PostgreSQL + PostGIS)
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "postgres")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "postgres")

    # App
    app_env: str = os.getenv("APP_ENV", "local")
    app_debug: bool = os.getenv("APP_DEBUG", "true").lower() == "true"

    # CORS
    # 環境変数が無ければローカルの典型オリジンをデフォルトに
    _default_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://[::1]:3000",
    ]
    _raw = os.getenv("APP_ORIGINS", "")
    app_origins: List[str] = (
        [o.strip() for o in _raw.split(",") if o.strip()] if _raw else _default_origins
    )

    # MinIO Storage Settings
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
    minio_bucket_name: str = os.getenv("MINIO_BUCKET_NAME", "trees")
    minio_secure : bool = False

    # SQLAlchemyを使ってPostgreSQLに接続するためのDSN接続文字列を組み立てるためのプロパティ
    @property
    def sync_pg_dsn(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings()