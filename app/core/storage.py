# /app/core/storage.py
from __future__ import annotations
from typing import IO
from abc import ABC, abstractmethod

class StoragePort(ABC):
    @abstractmethod
    def put_object(self, object_name: str, data: IO[bytes], length: int, content_type: str | None = None) -> None: ...
    @abstractmethod
    def remove_object(self, object_name: str) -> None: ...
    @abstractmethod
    def public_url(self, object_name: str) -> str: ...