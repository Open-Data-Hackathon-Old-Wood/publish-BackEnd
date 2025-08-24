# /app/post/pin/matsu/repository.py
from __future__ import annotations
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.post.pin.nara.schemas import PostPinRequest
from app.features.pins.models import Point
from app.features.pin_detail.matsu.models import PointDetailMatsu
from app.features.pin_detail.nara.models import PointDetailNara

# DB内のエラーを示すための例外クラス
class RepositoryError(RuntimeError):
    pass

# postGISへ書き込みを行い、1トランザクションでpointの親テーブルと, point_detail_matsuなどの子テーブルを作る
class PinRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # pinテーブルのdraftを作成. commitをしないで一時的に処理. fail時にはrollbackする
    def create_pin_draft(self, req: PostPinRequest) -> int:
        try:
            point_id = self._create_pin_without_commit(req)
            return point_id
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"DB draft insert failed: {e!s}") from e
    
    # pointを作成してflushでpostGISにテーブルを追加。ただしcommitを送らず、取り消せる状態にしておく。
    def _create_pin_without_commit(self, req: PostPinRequest):
        try:
            # point table creation
            point = Point(
                category=req.category,
                geom=func.ST_SetSRID(func.ST_MakePoint(req.lng, req.lat), 4326),
            )
            self.db.add(point)
            self.db.flush()

            # Natsuだったらpoint_details_matsuにrecordをinsert
            if req.category == "Matsu":
                detail = PointDetailMatsu(
                    point_id=point.id,
                    health_status=req.texture_rating,
                    notes="",
                )
                self.db.add(detail)
            elif req.category == "Nara":
                detail = PointDetailNara(
                    point_id=point.id,
                    needle_size=req.hole_size,
                    notes="",
                )
                self.db.add(detail)
            else:
                self.db.rollback()
                raise RepositoryError(f"Unknown category: {req.category}")
            
            return point.id

        except RepositoryError:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"DB write failed: {e!s}") from e