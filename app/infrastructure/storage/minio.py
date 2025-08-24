# app/infrastructure/storage/minio.py
from typing import IO
from minio import Minio
from minio.error import S3Error
from app.core.config import settings
from app.core.storage import StoragePort

class MinioStorage(StoragePort):
    def __init__(self) -> None:
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        self.bucket = settings.minio_bucket_name
        self._ensure_bucket()

    def _ensure_bucket(self) -> None:
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def put_object(self, object_name: str, data: IO[bytes], length: int, content_type: str | None = None) -> None:
        self.client.put_object(self.bucket, object_name, data, length, content_type=content_type)

    def remove_object(self, object_name: str) -> None:
        try:
            self.client.remove_object(self.bucket, object_name)
        except S3Error as e:
            if e.code not in {"NoSuchKey", "NoSuchObject"}:
                raise

    def public_url(self, object_name: str) -> str:
        scheme = "https" if settings.minio_secure else "http"
        return f"{scheme}://{settings.minio_endpoint}/{self.bucket}/{object_name}"