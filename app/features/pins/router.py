from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.features.pins.schemas import CircleQuery,PointOut,PointResponse
from app.features.pins.service import PinsService

router = APIRouter(prefix="/pins", tags=["pins"])

# リクエストで指定された位置情報を中心に、指定された半径内のポイントデータをDBから取得し、レスポンスとして返すエンドポイント
# long,latを139.767125,35.681236のように指定すると、東京駅の位置情報を中心に、半径200m以内のポイントデータを取得できる。

# マツ枯れのポイントデータを返すためのエンドポイント
@router.get("/matsu",response_model=PointResponse)
def get_matsu_pins(
    centerLng: float = Query(..., description="current longitude (WGS84)"),
    centerLat: float = Query(..., description="current latitude (WGS84)"),
    radius_m: float = Query(1000000.0, gt=0, description="search radius in meters"),
    zoom: int = Query(15, ge=0, le=22),
    cluster: bool = Query(False),
    pixel_bucket: int = Query(40, ge=8, le=128),
    pad_factor: float = Query(0.25, ge=0.0, le=1.0, description="prefetch radius ratio"),
    limit: int = Query(5000, ge=1, le=20000),
    category: str = "Matsu",
    start: str = Query(..., description="Start date in YYYY-MM-DD format (e.g., '2023-01-01')"),
    end: str = Query(..., description="End date in YYYY-MM-DD format (e.g., '2023-12-31')"),
    db: Session = Depends(get_db),
):
    query = CircleQuery(centerLng=centerLng, centerLat=centerLat, radius_m=radius_m, zoom=zoom,cluster=cluster, pixel_bucket=pixel_bucket, pad_factor=pad_factor,category=category,start=start,end=end,limit=limit)
    svc = PinsService(db)
    return svc.get_pins_nearby(query)

# ナラ枯れのポイントデータを返すためのエンドポイント
@router.get("/nara",response_model=PointResponse)
def get_nara_pins(
    centerLng: float = Query(..., description="current longitude (WGS84)"),
    centerLat: float = Query(..., description="current latitude (WGS84)"),
    radius_m: float = Query(10000.0, gt=0, description="search radius in meters"),
    zoom: int = Query(15, ge=0, le=22),
    cluster: bool = Query(False),
    pixel_bucket: int = Query(40, ge=8, le=128),
    pad_factor: float = Query(0.25, ge=0.0, le=1.0, description="prefetch radius ratio"),
    limit: int = Query(5000, ge=1, le=20000),
    category: str = "Nara",
    start: str = Query(..., description="Start date in YYYY-MM-DD format (e.g., '2023-01-01')"),
    end: str = Query(..., description="End date in YYYY-MM-DD format (e.g., '2023-12-31')"),
    db: Session = Depends(get_db),
):
    query = CircleQuery(centerLng=centerLng, centerLat=centerLat, radius_m=radius_m, zoom=zoom,cluster=cluster, pixel_bucket=pixel_bucket, pad_factor=pad_factor,category=category,start=start,end=end,limit=limit)
    svc = PinsService(db)
    return svc.get_pins_nearby(query)
