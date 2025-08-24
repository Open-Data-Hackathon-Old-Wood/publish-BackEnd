## app/features/pins/repository.py
from typing import Mapping
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.features.pins.models import Point
from datetime import datetime,timezone,timedelta
from zoneinfo import ZoneInfo


class PinsRepository:
    def __init__(self, db: Session):
        self.db = db

    # 3857座標系で指定された位置情報を中心に円を作成する
    @staticmethod
    def _buffer_3857(lng: float, lat: float, radius_m: float, pad_factor: float):
        p4326 = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
        p3857 = func.ST_Transform(p4326, 3857)
        r = radius_m * (1.0 + pad_factor)
        buf = func.ST_Buffer(p3857, r)
        return buf
    
    # 期間を指定して、範囲内のピンの緯度経度とidを返す。_buffer_3857を使用して円を作り、その中で交点を持つポイントデータを取得する。メルカトルとGPS座標の両方を使うことで、速度と精度を両立させる
    def fetch_points_by_category(self, *, lng: float, lat: float, radius_m: float, pad_factor: float, category: str,start: str,end: str, limit: int):
        buf = self._buffer_3857(lng, lat, radius_m, pad_factor)
        where_bbox = Point.geom.op("&&")(func.ST_Transform(buf, 4326))
        where_int = func.ST_Intersects(func.ST_Transform(Point.geom, 3857), buf)
        where_cat = (Point.category == category)
        where_duration = (
            (Point.created_at >= datetime.fromisoformat(start).replace(tzinfo=ZoneInfo("Asia/Tokyo"))) &
            (Point.created_at < datetime.fromisoformat(end).replace(tzinfo=ZoneInfo("Asia/Tokyo")) + timedelta(days=1))
        )
        stmt = (
            select(
                Point.id.label("id"),
                Point.category.label("category"),
                func.ST_X(Point.geom).label("lng"),
                func.ST_Y(Point.geom).label("lat"),
                Point.created_at.label("created_at"),
                Point.updated_at.label("updated_at"),
            )
            .where(where_bbox, where_int,where_cat,where_duration)
            .limit(limit)
        )
        result = list(self.db.execute(stmt).mappings().all())
        print(result)
        return result

    # # 指定された位置情報を中心に、指定された半径内のポイントデータをクラスタリングして取得する関数
    # def fetch_clusters(self,*,lon: float,lat: float,radius_m: float,pad_factor: float,cell_m: float,limit: int):
    #     buf = self._buffer_3857(lon, lat, radius_m, pad_factor)
    #     where_bbox = Pin.geom.op("&&")(func.ST_Transform(buf, 4326))
    #     where_int = func.ST_Intersects(func.ST_Transform(Pin.geom, 3857), buf)
    #     pts = (
    #         select(func.ST_Transform(Pin.geom, 3857).label("g"))
    #         .where(where_bbox, where_int)
    #         .limit(limit)
    #     ).cte("pts")

    #     cell = func.ST_SnapToGrid(pts.c.g, cell_m, cell_m).label("cell")
    #     center = func.ST_Centroid(func.ST_Collect(pts.c.g)).label("center")

    #     grid = (
    #         select(cell, func.count().label("count"), center)
    #         .select_from(pts)
    #         .group_by(cell)
    #     ).cte("grid")

    #     stmt = select(
    #         grid.c.count,
    #         func.ST_X(func.ST_Transform(grid.c.center, 4326)).label("lon"),
    #         func.ST_Y(func.ST_Transform(grid.c.center, 4326)).label("lat"),
    #     )
    #     return list(self.db.execute(stmt).mappings().all())