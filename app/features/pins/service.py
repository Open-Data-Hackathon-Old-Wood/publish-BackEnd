## app/features/pins/service.py
import math
from sqlalchemy.orm import Session
from app.features.pins.repository import PinsRepository
from app.features.pins.schemas import CircleQuery, PointResponse

class PinsService:
    def __init__(self, db: Session):
        self.repo = PinsRepository(db)

    @staticmethod
    def meters_per_pixel(zoom: int, lat: float) -> float:
        return 156543.03392 * math.cos(math.radians(lat)) / (2 ** zoom)

    # clusterが無効の場合は、指定された位置情報を中心に、指定された半径内のポイントデータをそのまま全件取得する
    def get_pins_nearby(self, query: CircleQuery):
        if not query.cluster:
            rows = self.repo.fetch_points_by_category(lng=query.centerLng, lat=query.centerLat, radius_m=query.radius_m, pad_factor=query.pad_factor, category=query.category,start=query.start,end=query.end,limit=query.limit)
            return PointResponse(items=rows)
        else:
            mpp = self.meters_per_pixel(query.zoom, query.centerLat)
            cell_m = query.pixel_bucket * mpp
            rows = self.repo.fetch_clusters(lon=query.centerLng, lat=query.centerLat, radius_m=query.radius_m,pad_factor=query.pad_factor, cell_m=cell_m,category=query.category, limit=query.limit)
        return PointResponse(items=rows)