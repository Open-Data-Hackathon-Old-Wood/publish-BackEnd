## app/features/images/repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.features.images.models import Image

class ImageRepository:
    def __init__(self, db: Session):
        self.db = db
    
    # DBから画像のURLを取得するメソッド. bucketとobject_keyを結合してURLを生成し、これをフロント側に渡す.point_idはユニークなので、photo_categoryも指定すればフェッチできる画像は１つだけ
    def fetch_image_by_point_id(self, *, point_id:int, photo_category:str) -> str:
        stmt = select(Image.bucket, Image.object_key).where(
            Image.point_id == point_id, Image.photo_category == photo_category
        ).limit(1)
        row = self.db.execute(stmt).first()
        # もし画像が存在しない場合は空文字列を返す
        if row is None:
            return ""
        bucket, object_key = row
        # ここでは仮にS3のURL形式を使用していると仮定
        return f"http://localhost:9000/{bucket}/{object_key}"
