## app/features/pin_detail/nara/repository.py
from typing import Mapping
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.features.pins.models import Point
from app.features.pin_detail.nara.models import PointDetailNara as Nara
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo

class NaraDetailRepository:
    def __init__(self, db: Session):
        self.db = db
    
    # 期間を指定して、指定された位置情報のピンIDを取得するメソッド。最新の一件を取得.ただしカテゴリーも検索対象に指定する
    def fetch_point_id(self, *, category:str = "Nara" ,lng: float, lat: float, start:str, end:str):
        where_point = func.ST_DWithin(
            Point.geom,
            func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326),
            0.0001  # 10m以内のピンを取得
        )
        # 期間を指定して、ピンIDを取得する。start: 2025-08-19, end: 2025-08-20であれば、2025-08-19 00:00:00から2025-08-20 23:59:59までの期間のピンを取得する
        where_duration = (
            (Point.created_at >= datetime.fromisoformat(start).replace(tzinfo=ZoneInfo("Asia/Tokyo"))) &
            (Point.created_at < datetime.fromisoformat(end).replace(tzinfo=ZoneInfo("Asia/Tokyo")) + timedelta(days=1))
        )
        where_category = (Point.category == category)
        stmt = (
            select(Point.id,Point.created_at)
            .where(where_point,where_duration, where_category) # 位置情報と期間、カテゴリーでフィルタリング
            .order_by(Point.created_at.desc())
            .limit(1)
        )
        return self.db.execute(stmt).mappings().one_or_none()
    
    # ピンの詳細情報をpoint_details_matsu tableから取得するメソッド. point_idはユニーク
    def fetch_point_detail(self, *, point_id: int):
        where_id = (Nara.point_id == point_id)
        stmt = (
            select(
                Nara.point_id,
                Nara.needle_size,  
            )
            .where(where_id)
            .limit(1)
        )
        return self.db.execute(stmt).mappings().one_or_none()