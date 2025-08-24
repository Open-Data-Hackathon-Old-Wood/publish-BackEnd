## app/features/pin_detail/matsu/service.py
from zoneinfo import ZoneInfo
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.features.pin_detail.matsu.repository import MatsuDetailRepository
from app.features.pin_detail.matsu.schemas import MatsuDetailQuery, MatsuDetailResponse,MatsuDetailOut,PhotoUrls
from app.features.pin_detail.matsu.models import PointDetailMatsu as Matsu
from app.features.images.schemas import ImageURLQuery, MatsuImageURLOut, NaraImageURLOut
from app.features.images.service import ImageService

class MatsuDetailService:
    def __init__(self, db: Session):
        self.repo = MatsuDetailRepository(db)

    # matsuのピンの詳細情報を取得するメソッド. 普通はPinがあればPinDetailもあるはずだけど、万が一Nullが返ってきた場合はstatus code 404を返す
    def get_pin_detail_matsu(self, query: MatsuDetailQuery):
        try:
            point = self.repo.fetch_point_id(category=query.category, lng=query.lng, lat=query.lat, start=query.start, end=query.end)
            if point is None:
                raise ValueError("No pin found at the specified location.")
            detail_info = self.repo.fetch_point_detail(point_id=point["id"])
            if detail_info is None:
                raise ValueError("No detail found for the specified pin.")
            
            matsu_image_service = ImageService(self.repo.db)
            image_query = ImageURLQuery(point_id=point["id"], photo_category="")
            image_urls = matsu_image_service.get_matsu_image_urls(image_query)

            # 画像URLは、pin_idを使って生成する。ここでは仮に"/images/pins/{point_id}.jpg"とする.
            return MatsuDetailResponse(
                id=str(point["id"]),
                category=query.category,
                lat=query.lat,
                lng=query.lng,
                start=query.start,
                end=query.end,
                texture_rating=detail_info["health_status"],
                hole_size=None,
                photo_urls=PhotoUrls(
                    whole_tree=[image_urls.wholeTree],
                    detail=[image_urls.detail],
                    base=[image_urls.base],
                    leaves=[image_urls.leaves],
                ),
                created_at=point["created_at"],
            )
            
        except ValueError as e:
            print(f"Error fetching pin details: {e}")
            return HTTPException(status_code=404, detail="Pin not found")
        except Exception as e:
            print(f"Unexpected error: {e}")
            return HTTPException(status_code=500, detail="Internal server error")
    