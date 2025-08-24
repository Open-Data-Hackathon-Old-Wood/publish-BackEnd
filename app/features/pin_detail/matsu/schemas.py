## app/features/pin_detail/matsu/schemas.py
from __future__ import annotations
from pydantic import BaseModel, Field, AwareDatetime, ConfigDict, field_serializer
from typing import Optional,Literal,Optional,List
from datetime import date,datetime,timezone


# Pinの詳細情報を取得するためのスキーマ
class MatsuDetailQuery(BaseModel):
    category: str = Field("matsu", description="Category of the wood (matsu or nara)")
    lat: float = Field(..., description="current latitude (WGS84)")
    lng: float = Field(..., description="current longitude (WGS84)")
    start: str = Field(..., description="Start date in YYYY-MM-DD format")
    end: str = Field(..., description="End date in YYYY-MM-DD format")


# マツガレのテーブルから詳細情報を返すためのスキーマ.詳細情報は１つのPinに対してしか返さないことを前提としている
class MatsuDetailOut(BaseModel):
    point_id: int
    health_status: int = Field(..., description="Needle size of the pine")
    created_at: AwareDatetime
    updated_at: AwareDatetime

class PhotoUrls(BaseModel):
    whole_tree: List[str] = Field(default_factory=list, serialization_alias="wholeTree")
    detail: List[str] = Field(default_factory=list)
    base: List[str] = Field(default_factory=list)
    leaves: List[str] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)

# レスポンスのスキーマ.画像のURLを含めて渡す
class MatsuDetailResponse(BaseModel):
    id: str
    category: Literal["Matsu"] | str
    lat: float
    lng: float
    start: str
    end: str
    texture_rating: int = Field(serialization_alias="textureRating")
    hole_size: Optional[int] = Field(default=None, serialization_alias="holeSize")
    photo_urls: PhotoUrls = Field(serialization_alias="photoUrls")
    created_at: datetime = Field(serialization_alias="createdAt")
    model_config = ConfigDict(populate_by_name=True)
