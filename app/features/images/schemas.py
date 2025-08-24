## app/features/images/schemas.py
from pydantic import BaseModel, Field

# 画像のURLを取得するためのスキーマ
class ImageURLQuery(BaseModel):
    point_id: int = Field(..., description="ID of the point to fetch images for")
    photo_category: str = Field(..., description="Category of the photo (e.g., wholeTree, detail, base, leaves)")


# 画像のURLを出力するスキーマ。ただし他のエンドポイントのレスポンスとして返すので、ここではResponseModelではなく、単なるPydanticモデルとして定義
class MatsuImageURLOut(BaseModel):
    wholeTree: str = Field(..., description="Whole tree image URL")
    leaves: str = Field(..., description="Leaves image URL")
    detail: str = Field(..., description="Detail image URL")
    base: str = Field(..., description="Base image URL")

class NaraImageURLOut(BaseModel):
    wholeTree: str = Field(..., description="Whole tree image URL")
    detail: str = Field(..., description="Detail image URL")
    base: str = Field(..., description="Base image URL")