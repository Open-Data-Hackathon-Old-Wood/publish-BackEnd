## app/features/pins/schema.py
from pydantic import BaseModel, Field, AwareDatetime

class CircleQuery(BaseModel):
    centerLng: float
    centerLat: float
    radius_m: float = Field(gt=0, default=1000.0)
    zoom: int = 15
    cluster: bool = True
    pixel_bucket: int = 40          # クラスタリングに使用するピクセル数
    pad_factor: float = 0.25        # 余白の比率
    category: str = Field(..., description="Category of the pin (e.g., 'Matsu', 'Nara')")
    start: str = Field(..., description="Start date in YYYY-MM-DD format (e.g., '2023-01-01')")
    end: str = Field(..., description="End date in YYYY-MM-DD format (e.g., '2023-12-31')")
    limit: int = 5000

class PointOut(BaseModel):
    id: int
    category: str
    lng: float
    lat: float
    created_at: AwareDatetime
    updated_at: AwareDatetime
    # model_config = dict(from_attributes=True) # type: ignore

# class PinClusterOut(BaseModel):
#     count: int
#     lon: float
#     lat: float

class PointResponse(BaseModel):
    items: list[PointOut]