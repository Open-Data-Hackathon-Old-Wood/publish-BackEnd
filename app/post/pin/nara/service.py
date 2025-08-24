# /app/post/pins/matsu/service.py
from __future__ import annotations
from typing import List, Optional, Dict
from uuid import uuid4
from io import BytesIO
from fastapi import UploadFile
from sqlalchemy.orm import Session
from .repository import PinRepository, RepositoryError
from app.post.pin.nara.schemas import PostPinRequest
from app.core.storage import StoragePort
from app.features.images.models import Image
from app.core.config import settings

# PostGISとMinIOを同時に書き込むためのクラス
class PinWriteService:
    def __init__(self, db: Session, storage: StoragePort):
        self.db = db
        self.repo = PinRepository(db)
        self.storage = storage
    
    # PostGISテーブルを作成し、MinIOにデータをアップロードする関数
    def create_pin_with_images(self, req: PostPinRequest):
        uploaded_keys: Dict[str, List[str]] = {"wholeTree": [], "detail": [], "base": [], "leaves": []}

        try:
            point_id = self.repo.create_pin_draft(req)
            groups: Dict[str, Optional[List[UploadFile]]] = {
                "wholeTree": req.whole_tree,
                "detail": req.detail,
                "base": req.base,
                "leaves": req.leaves,
            }
            for group, files in groups.items():
                if not files:
                    continue
                for f in files:
                    content = f.file.read()
                    f.file.seek(0)
                    if not content:
                        continue
                    object_name = f"{point_id}/{group}/{uuid4()}_{f.filename or 'blob'}"
                    self.storage.put_object(object_name, BytesIO(content), len(content), content_type=f.content_type)
                    uploaded_keys[group].append(object_name)

            for group, keys in uploaded_keys.items():
                for key in keys:
                    url = self.storage.public_url(key)
                    image = Image(
                        point_id=point_id,
                        bucket=getattr(self.storage, "bucket", settings.minio_bucket_name),
                        object_key=key,                 # MinIOに保存したオブジェクトキー
                        photo_category=group,           # 'wholeTree' | 'detail' | 'base' | 'leaves'
                    )
                    self.db.add(image)

            # ここまで成功したらPostGISにcommitする
            self.db.commit()
        
        #　例外が発生した際は、commitせず、バケットにアップロードした画像を削除して、PostGISの中身をロールバックする。
        except Exception as e:
            for keys in uploaded_keys.values():
                for key in keys:
                    try:
                        self.storage.remove_object(key)
                    except Exception:
                        pass
            self.db.rollback()
            raise RepositoryError(f"Failed to create pin with images: {e!s}")